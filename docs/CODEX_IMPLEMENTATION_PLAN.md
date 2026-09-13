# T4 — Kế hoạch triển khai tối thiểu Round 2 MVP

Status: PROPOSED — chờ ChatGPT Team Lead phê duyệt trước T5.
Owner: Codex — Implementation Engineer.

Tôi đã đọc đầy đủ năm tài liệu bắt buộc, theo đúng thứ tự, sau khi đọc docs/PROMPT_CODEX_IMPLEMENTATION_PLAN.md:

1. [AGENTS.md](../AGENTS.md)
2. [docs/ROUND2_PRODUCT_SPEC.md](ROUND2_PRODUCT_SPEC.md)
3. [docs/ROUND2_REQUIREMENTS_TRACE.md](ROUND2_REQUIREMENTS_TRACE.md)
4. [docs/DECISION_LOG.md](DECISION_LOG.md)
5. [docs/TASKS.md](TASKS.md)

Product Spec và decisions D-001 đến D-009 là FROZEN. T4 chỉ tạo và commit docs/CODEX_IMPLEMENTATION_PLAN.md; các file triển khai được liệt kê bên dưới chỉ là đề xuất cho giai đoạn sau khi kế hoạch được duyệt. Không thay đổi spec, requirements trace, decision log hoặc Task Board.

Luồng bắt buộc: Buyer AI Request -> Intent Decoder -> Structured Intent -> Product-level Eligibility -> Semantic Catalogue Matching -> Merchant Offer Scenario Generation -> Offer-level Buyer + Merchant Feasibility -> Offer Scoring / Selection -> Machine-readable B2A Offer -> Buyer Accept -> Synthetic Transaction Handoff (transaction_ready).

Product-level eligibility chạy trước tối ưu, loại các điều kiện bất biến/bất khả thi như hết hàng, giao hàng không kịp hoặc capability bắt buộc không đạt. Không loại sản phẩm chỉ vì base_price vượt budget hay base warranty chưa đủ nếu offer có thể điều chỉnh hợp lệ. Offer-level feasibility chạy sau khi sinh scenario, kiểm tra buyer_total_price, warranty, delivery, stock, các hard requirements và merchant economics. Điểm semantic cao không thể vượt qua hard constraints; evidence không có vẫn là unverified.

Các giới hạn/gaps đã chấp nhận trong Requirements Trace, không triển khai mở rộng nếu chưa có quyết định mới được Team Lead phê duyệt:

- R2-08 — PARTIAL: chỉ synthetic order_intent/transaction_ready, không production checkout, real payment hoặc payment API/backend.
- R2-09 — PARTIAL / STRETCH: không triển khai negotiation trong kế hoạch core này; single counter-offer chỉ được xem xét riêng sau khi core đạt acceptance; không multi-round autonomous negotiation.
- R2-10 — GAP ACCEPTED: mỗi offer chỉ một laptop; không dynamic multi-product bundling.
- R2-11: không có live LLM-to-LLM agent pair; JSON contracts và Streamlit minh họa tương tác B2A.
- Chỉ fictional laptop catalogue; không multi-category, multi-merchant, scraping, tích hợp retailer/FPT thật hoặc dữ liệu khách hàng thật.
- R2-03/R2-12: buyer_fit và economics là chỉ số minh họa, không dự đoán xác suất mua thật, không tuyên bố sales uplift, ranking accuracy hoặc hiểu proprietary shopping-agent ranking.
- External LLM là tùy chọn; khả năng demo không phụ thuộc API key. Source PDFs tiếp tục nằm ngoài public repository theo D-004/D-009.

Ưu tiên: end-to-end demo -> đúng deterministic constraints/economics -> fallback tin cậy -> core tests/failure handling -> code người mới học Python giải thích được -> UI polish.

## Kiến trúc và cấu hình đề xuất

Giữ bảy file cốt lõi: app.py, requirements.txt, data/catalog.csv, src/intent.py, src/matcher.py, src/optimizer.py, tests/test_core.py. Sau phê duyệt, bổ sung .gitignore cho secrets/cache và README.md cho tài liệu bắt buộc. Không tạo thêm schema/service/config module, database hoặc framework backend.

app.py chỉ điều phối và hiển thị. Ba module src dùng hàm thuần với dict/list và validation tường minh; không phụ thuộc Streamlit. src/matcher.py kiêm đọc/kiểm tra CSV. src/optimizer.py kiêm tạo B2A response và handoff thuần để tránh thêm file. Giữ ranh giới này giúp kiểm thử mà không cần chạy UI; gộp tất cả vào app.py không đem lại lợi ích đủ lớn.

Stack: Python + Streamlit + Pandas + pytest; Gemini API tùy chọn. Không React, Next.js, FastAPI, authentication, Docker, microservices hoặc real payment.

Các giá trị sau là cấu hình demo ĐỀ XUẤT để Team Lead duyệt cùng kế hoạch, không phải thay đổi hay tuyên bố thêm frozen decisions:

- discount_rates: 0%, 3%, 5%; buyer shipping fee: mức catalogue hoặc 0; warranty: base hoặc extension có khai báo. Tối đa 12 tổ hợp/sản phẩm trước loại trùng.
- min_margin_rate: 0.10, cấu hình synthetic; alpha = beta = 0.5 cho buyer fit và economic score.
- Preference range 0..1: neutral 0.5; ưu tiên cao được nói rõ 0.9, ưu tiên thấp được nói rõ 0.3. Ghi assumptions khi áp dụng default. use-case weight 1.0; chuẩn hóa tổng trọng số trước khi kết hợp các component 0..1. Không suy diễn ưu tiên chính xác từ thông tin không có.
- Min-max normalization trả 0.5 khi mọi giá trị bằng nhau, kể cả tập chỉ có một offer. Tập rỗng được xử lý trước normalization. Tie-break: offer_score giảm dần, buyer_total_price tăng dần, rồi product_id và offer_id.
- Tiền AUD dùng Decimal từ dữ liệu chuỗi; làm tròn offer_price đến cent bằng ROUND_HALF_UP trước feasibility; không làm tròn margin để quyết định đạt/rớt. Giá trị hiển thị được định dạng riêng.

## Các bước triển khai sau khi T4 được duyệt

T5.1–T5.11 là subtask đề xuất của T5, giữ thứ tự trong TASKS.md. Mỗi phần bổ sung test cho hành vi vừa có; T5.11 hoàn tất coverage và kiểm thử tích hợp. Những lệnh kiểm tra dưới đây là dự kiến, chưa được chạy trong T4.

### T5.1 — Khung chạy và dependencies

- **Task ID:** T5.1
- **Files tạo/sửa:** Tạo app.py, requirements.txt, .gitignore.
- **Mục đích:** Có điểm khởi chạy Streamlit tối thiểu và môi trường có thể tái lập.
- **Inputs:** D-003, kiến trúc và quy tắc secrets đã frozen.
- **Outputs:** Ứng dụng khởi động được; dependency versions được ghi sau khi kiểm chứng lúc triển khai.
- **Cách triển khai:** Dùng đúng stack đã duyệt. Chỉ tạo khung app ở bước này. .gitignore loại .env, .streamlit/secrets.toml, môi trường ảo và cache; secrets lấy từ environment hoặc Streamlit secrets. Không có key trong source, fixture hoặc log.
- **Tests/verification:** Cài dependencies trong môi trường sạch; python -m streamlit run app.py; git check-ignore cho các đường dẫn secrets; kiểm tra Git diff chỉ chứa file dự kiến.
- **Phụ thuộc:** T4 được ChatGPT Team Lead phê duyệt; T0–T3 đã hoàn thành.
- **Implementation risk:** LOW

### T5.2 — Catalogue laptop synthetic và validation

- **Task ID:** T5.2
- **Files tạo/sửa:** Tạo data/catalog.csv, src/matcher.py, tests/test_core.py.
- **Mục đích:** Cung cấp dữ liệu nhỏ nhưng thể hiện đủ đánh đổi và failure cases.
- **Inputs:** Catalogue schema tại Product Spec §7.
- **Outputs:** Tám laptop fictional hợp lệ; hàm load/validate catalogue; fixture lỗi riêng trong tests.
- **Cách triển khai:** CSV có đủ product_id, name, description, base_price, unit_cost, stock, delivery_days, merchant_shipping_cost, buyer_shipping_fee, base_warranty_years, extended_warranty_years, extended_warranty_cost, performance_score, portability_score, battery_score, tags, evidence_notes. Pandas đọc dữ liệu; kiểm tra ID duy nhất, kiểu, số hữu hạn và range. Không biến numeric thiếu thành 0. Hai trường extension cùng vắng nghĩa là không có lựa chọn extension; khai báo thiếu một phần là dữ liệu lỗi. Dữ liệu thể hiện baseline feasible, base_price vượt budget có thể giảm hợp lệ, shipping làm vượt budget, margin thấp, stock zero, delivery trễ, thiếu extension và evidence thiếu; một sản phẩm có thể phục vụ nhiều tình huống. Evidence trong catalogue luôn được nhận diện là synthetic.
- **Tests/verification:** Schema/ID/range; numeric thiếu, NaN hoặc vô cực; extension thiếu trường; catalogue hợp lệ có tám sản phẩm; dữ liệu lỗi được báo rõ và không chạy selection trên dữ liệu không tin cậy.
- **Phụ thuộc:** T5.1.
- **Implementation risk:** LOW

### T5.3 — Intent decoder, controlled mapping và fallback

- **Task ID:** T5.3
- **Files tạo/sửa:** Tạo src/intent.py; sửa requirements.txt và tests/test_core.py.
- **Mục đích:** Buyer request trở thành validated structured intent với hoặc không với external API.
- **Inputs:** Buyer request; preset hoặc structured input do người dùng chọn; API key tùy chọn; schema §6.
- **Outputs:** Decoded intent gồm hard_requirements, preferences, requested_attributes, unresolved_requirements, assumptions; intent_mode và lý do fallback.
- **Cách triển khai:** Xây controlled semantic mapping/preset trước, rồi adapter Gemini tùy chọn có timeout hữu hạn. Một validator dùng chung cho cả ba đường. Mapping hiểu cụm đồng nghĩa về gaming/GPU, portability và battery; parse budget/delivery/warranty, kiểm tra kiểu/range và ý nghĩa. Khi có key và người dùng chạy request, thử LLM; không key/API lỗi/JSON lỗi chuyển controlled mapping. Nếu vẫn không hiểu, giữ phần chưa rõ và cho chọn preset/structured input, không âm thầm thay request. Giá trị thiếu giữ null; hard requirement chưa giải quyết không được xác nhận đã đạt. intent_mode dùng llm, controlled_mapping, fallback_preset; UI nhãn tương ứng LLM mode, controlled mapping, fallback preset. Prompt chỉ chứa request/schema/từ vựng semantic cần thiết; không chứa unit_cost, margin threshold hay merchant economics. Giải thích offer dùng deterministic facts.
- **Tests/verification:** Một cặp paraphrase cùng constraints và ưu tiên tương đương; neutral defaults/assumptions; missing/null và unsupported requirements; mock LLM hợp lệ, JSON sai, kiểu/range sai, timeout/API lỗi; không key vẫn chạy; kiểm tra prompt không chứa merchant economics; fallback không tự nới hard constraints.
- **Phụ thuộc:** T5.2.
- **Implementation risk:** MEDIUM

### T5.4 — Product-level eligibility và semantic matching

- **Task ID:** T5.4
- **Files tạo/sửa:** Sửa src/matcher.py và tests/test_core.py.
- **Mục đích:** Tách sản phẩm bất khả thi khỏi ứng viên rồi tính buyer fit có thể giải thích.
- **Inputs:** Validated catalogue và structured intent.
- **Outputs:** Eligible candidates, rejected products với reason, component scores và evidence/unresolved facts.
- **Cách triển khai:** Áp dụng D-005: loại stock <= 0, delivery bất khả thi, capability bắt buộc không đạt hoặc mandatory attribute được biết là false. Chưa áp budget theo base_price; chưa loại vì base warranty khi extension được khai báo. Tính use_case_fit rõ ràng từ tag compatibility cùng performance/portability/battery fit; weighted combination theo các ưu tiên đã công bố. Giữ toàn bộ candidates eligible trong catalogue tám sản phẩm cho bounded search, tránh top-k nhỏ làm mất offer khả thi. Evidence thiếu là unverified; chuyển tiếp để offer-level xử lý, không biến thành positive claim.
- **Tests/verification:** Stock zero; delivery/capability fail; giữ sản phẩm base_price vượt budget; giữ sản phẩm có extension phù hợp; explicit use_case_fit và thay đổi ưu tiên ảnh hưởng ranking; unverified được giữ; zero eligible candidates không crash.
- **Phụ thuộc:** T5.3.
- **Implementation risk:** MEDIUM

### T5.5 — Bounded merchant offer scenario generation

- **Task ID:** T5.5
- **Files tạo/sửa:** Tạo src/optimizer.py; sửa tests/test_core.py.
- **Mục đích:** Tạo các phương án merchant-controlled hữu hạn thay vì chỉ trả SKU.
- **Inputs:** Eligible candidates và scenario rules được duyệt cùng kế hoạch.
- **Outputs:** Các scenario có offer_id ổn định, giá, shipping fee, warranty và incremental cost.
- **Cách triển khai:** Duyệt tổ hợp discount 0/3/5%, buyer shipping fee hiện tại/0, base/declared extension; loại trùng. Extension là tổng warranty_years được khai báo, không tự cộng thêm năm tùy ý. Base scenario có warranty_incremental_cost = 0; extension dùng đúng extended_warranty_cost. merchant_shipping_cost giữ nguyên ở cả free-shipping scenario. ID xác định từ product và điều kiện offer.
- **Tests/verification:** Có hơn một scenario cho ít nhất một candidate; tối đa 12 tổ hợp mỗi sản phẩm trước loại trùng; không discount/warranty tùy ý; không extension nếu thiếu khai báo; giữ merchant shipping cost; ID và kết quả lặp lại ổn định.
- **Phụ thuộc:** T5.4.
- **Implementation risk:** MEDIUM

### T5.6 — Offer-level buyer/merchant feasibility và economics

- **Task ID:** T5.6
- **Files tạo/sửa:** Sửa src/optimizer.py và tests/test_core.py.
- **Mục đích:** Chỉ giữ offer đáp ứng toàn bộ hard buyer requirements và merchant economics.
- **Inputs:** Scenarios, validated intent, catalogue facts và min_margin_rate.
- **Outputs:** Feasible offers có economics chính xác và rejected scenarios với reason codes.
- **Cách triển khai:** Tính deterministic: buyer_total_price = offer_price + buyer_shipping_fee; contribution = buyer_total_price - unit_cost - merchant_shipping_cost - warranty_incremental_cost; contribution_margin_rate = contribution / buyer_total_price khi total > 0. Kiểm tra budget trên tổng tiền buyer; kiểm tra lại stock, delivery, warranty và các hard requirements trên từng offer. Loại contribution < 0, total <= 0 hoặc margin dưới ngưỡng. Free shipping chỉ đặt buyer_shipping_fee = 0, không xóa merchant cost. Một hard requirement cần evidence nhưng còn unverified không được coi là satisfied: trả nhánh không có offer được xác nhận khả thi cùng unresolved reason. Numeric lỗi được báo validation error, không thay bằng số giả định để tạo offer.
- **Tests/verification:** Tính tay case tiền/chi phí/biên margin; đúng tại budget và margin threshold, sai khi vượt/thiếu; base_price vượt budget được discount cứu; base_price trong budget nhưng shipping làm fail; free shipping và warranty cost giảm contribution đúng; contribution âm/zero total; high-fit infeasible bị loại; unverified hard requirement không được thông qua.
- **Phụ thuộc:** T5.5.
- **Implementation risk:** HIGH

### T5.7 — Offer scoring và selection

- **Task ID:** T5.7
- **Files tạo/sửa:** Sửa src/optimizer.py và tests/test_core.py.
- **Mục đích:** Chọn offer tốt nhất trong tập khả thi bằng logic công bố và lặp lại được.
- **Inputs:** Chỉ feasible scenarios, buyer-fit components và contribution margin.
- **Outputs:** Recommended offer, normalized component scores và lý do selection.
- **Cách triển khai:** Economic score lấy contribution_margin_rate. Chuẩn hóa buyer fit và economic score trước khi cộng với alpha/beta. Dùng equal-value handling và tie-break đã nêu. Không score/rank để cứu hard failure; rỗng trả no-feasible result trước normalization. Output hiển thị điểm là minh họa, không phải purchase probability.
- **Tests/verification:** Empty set, single offer, all-equal values, khác đơn vị và tie-break; selection ổn định khi lặp/chuyển thứ tự input; semantic ưu tiên thực sự ảnh hưởng kết quả trong fixture phù hợp; offer infeasible không thể thắng.
- **Phụ thuộc:** T5.6.
- **Implementation risk:** MEDIUM

### T5.8 — Machine-readable B2A offer response

- **Task ID:** T5.8
- **Files tạo/sửa:** Sửa src/optimizer.py và tests/test_core.py.
- **Mục đích:** Tạo tailored merchant proposal theo schema §14.
- **Inputs:** Validated intent, selected offer hoặc failure reason, evidence và intent_mode.
- **Outputs:** JSON offer_available hoặc no_feasible_offer, kèm giải thích ngắn dựa trên structured facts.
- **Cách triển khai:** Hàm thuần tạo đầy đủ decoded_intent, recommended_offer, buyer_match, merchant_constraints, evidence, unresolved_requirements, intent_mode ở success response. Hai nhánh không có eligible product và có candidates nhưng không có feasible scenario dùng reason phân biệt rõ. Bảo toàn null/unverified; JSON money nhất quán với giá đã kiểm tra; không xuất NaN/Infinity. Buyer response chỉ công bố constraint status, không tiết lộ private unit_cost hoặc margin threshold. Không dùng LLM để quyết định/sửa facts của response.
- **Tests/verification:** Schema keys/types và JSON serialization; buyer_total_price khớp offer; evidence/mode không bị mất; explanations không claim thuộc tính chưa xác minh; phân biệt hai failure reasons; không private economics trong buyer response.
- **Phụ thuộc:** T5.7.
- **Implementation risk:** LOW

### T5.9 — Buyer Accept và synthetic transaction handoff

- **Task ID:** T5.9
- **Files tạo/sửa:** Sửa src/optimizer.py và tests/test_core.py.
- **Mục đích:** Đóng vòng B2A chỉ sau khi buyer chấp nhận feasible offer hiện hành.
- **Inputs:** Current feasible offer, accepted offer_id và explicit acceptance.
- **Outputs:** transaction_ready với order_intent theo §15 và payment_status = not_processed_demo.
- **Cách triển khai:** Hàm thuần tạo synthetic order_id từ accepted offer; giữ offer_id, product_id, quantity = 1, buyer_total_price và currency = AUD. Kiểm tra offer thuộc current result và đã accepted; không tạo handoff nếu thiếu offer, offer không khả thi hoặc ID không khớp. Chỉ tạo object JSON, không gọi checkout/payment service và không mô phỏng thành thanh toán thật.
- **Tests/verification:** Chưa accept không có handoff; reject no-offer/wrong ID; toàn bộ order facts khớp accepted offer; cùng input cho handoff xác định; quantity/currency/payment status đúng.
- **Phụ thuộc:** T5.8.
- **Implementation risk:** MEDIUM

### T5.10 — Streamlit end-to-end UI

- **Task ID:** T5.10
- **Files tạo/sửa:** Sửa app.py và tests/test_core.py.
- **Mục đích:** Có demo chạy được từ buyer request đến transaction_ready, ưu tiên luồng core trước trang trí.
- **Inputs:** Request/preset/structured input, catalogue, kết quả các module.
- **Outputs:** Đủ chín UI surfaces tại §18, success flow và thông báo failure rõ ràng.
- **Cách triển khai:** Nối đúng thứ tự pipeline. Hiển thị Buyer Agent Request, mode thực tế, Decoded Intent, candidates/rejection reasons, Recommended Merchant Offer, buyer-fit/merchant explanation, offer JSON, Buyer Accept và synthetic transaction JSON. Dùng st.session_state cho current offer/acceptance; khi request/preset thay đổi hoặc chạy lại pipeline, xóa acceptance/handoff cũ và vô hiệu Accept cho đến khi có offer hiện hành. Không có key vẫn hoàn tất demo bằng mapping/preset. Gắn nhãn synthetic/illustrative cho catalogue, economics và transaction; UI là merchant demo surface.
- **Tests/verification:** Chạy python -m streamlit run app.py từ trạng thái sạch không có key, request gaming budget 1300/delivery 3/warranty 2 đến accept/transaction_ready; một failure scenario; đổi request sau accept không dùng offer cũ; nút Accept chỉ bật đúng; kiểm tra đủ surfaces và nhãn mode. Thêm UI state test bằng công cụ test tích hợp của Streamlit nếu phiên bản đã chọn hỗ trợ; vẫn giữ trong tests/test_core.py.
- **Phụ thuộc:** T5.9.
- **Implementation risk:** MEDIUM

### T5.11 — Hoàn tất core tests và failure handling

- **Task ID:** T5.11
- **Files tạo/sửa:** Sửa tests/test_core.py; các regression fix cần thiết chỉ sửa đúng hàm đã triển khai trong app.py, src/intent.py, src/matcher.py hoặc src/optimizer.py theo lỗi thực tế, không thêm file.
- **Mục đích:** Xác nhận toàn bộ acceptance criteria thay vì chỉ các module riêng lẻ.
- **Inputs:** Pipeline/UI hoàn chỉnh, synthetic catalogue, fixtures và mock API.
- **Outputs:** Bộ unit/integration tests và kết quả chạy thực tế để T6 review.
- **Cách triển khai:** Bổ sung integration test request -> intent -> eligibility -> match -> scenarios -> feasibility -> selection -> B2A -> accept -> handoff. API được mock để test suite chạy offline. Kiểm tra các biên economics với expected values tính tay. Các test trước đó đã chạy theo bước; bước này đối chiếu đủ 23 acceptance criteria. Nếu xuất hiện P0 chưa có cách giải quyết đúng frozen spec, dừng và báo Team Lead.
- **Tests/verification:** python -m pytest -q; smoke test app fresh-start success và failure. Bao phủ API unavailable/invalid JSON, paraphrase, no eligible product, no economically feasible offer, stock zero, budget/shipping/warranty, missing numeric/evidence, zero/equal normalization, stale/unaccepted handoff. Kiểm tra git diff và git ls-files để loại secrets và file ngoài phạm vi. Chỉ báo pass cho lệnh thực sự đã chạy.
- **Phụ thuộc:** T5.10.
- **Implementation risk:** MEDIUM

### T8 — README nháp và bàn giao tài liệu kỹ thuật

- **Task ID:** T8
- **Files tạo/sửa:** Tạo README.md; không sửa docs/SUBMISSION_CHECKLIST.md hoặc pitch/PITCH_CONTENT.md thuộc Team Lead.
- **Mục đích:** Người mới học Python có thể cài, chạy và giải thích demo; đáp ứng R2-14.
- **Inputs:** Implementation cuối cùng, cấu hình đã duyệt, kết quả T5 và các sửa lỗi được duyệt qua T6/T7.
- **Outputs:** README nháp để ChatGPT Team Lead duyệt cuối.
- **Cách triển khai:** Ghi kiến trúc/file responsibilities, flow/schema, economics, weights/defaults/tie-break, scenario bounds, công nghệ/dependencies/API và nguồn bên ngoài; setup/run/test, environment/Streamlit secrets, ba execution modes, synthetic disclosure và accepted gaps. Không mô tả planned feature/test thành đã triển khai/đã pass. README nêu rõ synthetic handoff không thực hiện thanh toán.
- **Tests/verification:** Làm theo README trong môi trường sạch không có key; chạy primary demo và failure scenario; kiểm tra danh sách thư viện/API khớp requirements, không có secrets; Team Lead review README trước final.
- **Phụ thuộc:** T5 hoàn tất; cập nhật theo kết quả T6/T7 trước duyệt cuối và T9.
- **Implementation risk:** LOW

## Trace và điểm bàn giao

| Requirements Trace | Bước triển khai / bằng chứng |
|---|---|
| R2-01, R2-06, R2-11, R2-17 | T5.8–T5.10: merchant-side flow, structured response và handoff; không thêm live agent pair/backend. |
| R2-02, R2-03 | T5.3–T5.4, T5.11: validated intent, mode minh bạch, use_case_fit và paraphrase test. |
| R2-04, R2-07 | T5.2–T5.4, T5.6, T5.8: catalogue, two-stage constraints, evidence và rejection reasons. |
| R2-05, R2-12 | T5.5–T5.7: bounded scenarios, contribution/margin, normalized buyer fit và final selection. |
| R2-08 | T5.9–T5.10: synthetic acceptance/handoff; giữ PARTIAL coverage đã chấp nhận. |
| R2-09, R2-10 | Không triển khai negotiation/bundling trong core plan. |
| R2-13, R2-16 | T5.1, T5.3, T5.10–T5.11: fresh-start demo, offline fallback, tests, secrets handling. |
| R2-14 | T8: README nháp của Codex, ChatGPT duyệt cuối. |
| R2-15 | Source code thuộc T5 sau phê duyệt; pitch/final deck và submission coordination thuộc Team Lead/User. |

T6 do ChatGPT Red Team/QA thực hiện. T7 chỉ sửa grounded P0/P1 do Team Lead chọn và phê duyệt; exact files của các sửa lỗi này chỉ được xác định sau review, không suy đoán trước hoặc thay Task Board. T9 thuộc User. Không cần đóng accepted gaps để chuyển MVP sang review.

T4 hoàn thành bằng commit duy nhất file kế hoạch này. Kiểm tra bàn giao: đủ năm mandatory readings, đủ chín trường cho từng implementation step, đúng thứ tự T5, accepted gaps được ghi rõ, diff chỉ có docs/CODEX_IMPLEMENTATION_PLAN.md. Đây là kiểm tra tài liệu; không chạy hay tuyên bố đã pass product tests vì chưa triển khai sản phẩm.

Dừng sau khi commit kế hoạch và chờ ChatGPT Team Lead phê duyệt. Commit T4 không đồng nghĩa T5 đã được phê duyệt.
