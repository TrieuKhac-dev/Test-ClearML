# Bộ công cụ & công nghệ cho dự án

## Backend (Java Spring)

### Spring Framework

- Spring MVC: Xây dựng ứng dụng web theo mô hình MVC.
- Spring Boot: Khởi tạo và cấu hình ứng dụng nhanh chóng.
- Spring Data JPA: Làm việc với cơ sở dữ liệu, ORM (mặc định dùng Hibernate).
- Spring Security: Xác thực, phân quyền, bảo mật ứng dụng.
- Spring Cloud: Công cụ cho microservices (service discovery, config server…).
- **Spring AI**: Tích hợp AI, xây dựng chatbot, kết nối các mô hình AI (OpenAI, Azure, HuggingFace, v.v.).
- **JWT**: Xác thực và phân quyền dựa trên token.
- **Keycloak**: Quản lý xác thực, SSO, tích hợp OAuth2/OpenID Connect.
- **Lombok**: Giảm boilerplate code (getter/setter, builder, v.v.).
- **Log4j 2 / SLF4j**: Logging hiệu quả, cấu hình linh hoạt.
- **ModelMapper / MapStruct**: Mapping giữa DTO và entity.
- **API Gateway**: Quản lý, điều phối request (Spring Cloud Gateway hoặc Kong, NGINX).
- **Rate Limiting**: Giới hạn số lượng request (Resilience4j, Bucket4j, hoặc tích hợp tại API Gateway).
- **Payment Gateway**: Tích hợp thanh toán (VD: Stripe, PayPal, VNPay, MoMo...)
  **Spring Actuator**: Theo dõi health và metrics của ứng dụng.

## Build & IDE

- **Gradle**: Công cụ build và quản lý dependency.
- **IntelliJ IDEA**: IDE chính cho phát triển Java.

## Testing (Java)

- **JUnit**: Unit test cho Java.
- **Mockito**: Mocking framework hỗ trợ kiểm thử.
- **Testcontainers**: Chạy test với môi trường thực trong container.
- **OWASP Dependency-Check**: Phát hiện lỗ hổng bảo mật trong dependency (tích hợp vào build pipeline).
- **Snyk**: Phát hiện lỗ hổng bảo mật, license issue, tích hợp trực tiếp vào CI/CD, có fix suggestion.

## Quản lý dependency

- **Renovate / Dependabot**: Bot tự động cập nhật dependency.

## Code Quality & Static Analysis

**Java**:

- SpotBugs: Phân tích mã tĩnh, phát hiện bug tiềm ẩn.
- Checkstyle: Kiểm tra coding convention.
- PMD: Phát hiện code smell.
- SonarQube: Nền tảng quản lý chất lượng mã, tích hợp nhiều công cụ phân tích.
- JavaDoc: Sinh tài liệu cho Java.
- Lombok: Giảm code lặp lại, cần kiểm tra warning khi phân tích mã tĩnh.
- Log4j 2 / SLF4j: Kiểm tra cấu hình logging, phát hiện log injection.
- ModelMapper / MapStruct: Đảm bảo mapping đúng giữa các lớp.

**JavaScript / TypeScript**:

- ESLint: Linting cho JS/TS.
- Prettier: Format code tự động.
- JSDoc: Sinh tài liệu cho JS/TS.
- Redux DevTools: Debug state Redux.

## Database

- **PostgreSQL / MySQL**: Cơ sở dữ liệu quan hệ phổ biến.
- **MongoDB**: Cơ sở dữ liệu NoSQL dạng document.
- **Elasticsearch**: Công cụ tìm kiếm và phân tích dữ liệu.

## Bất đồng bộ & Messaging

- **Apache Kafka**: Event streaming, xử lý bất đồng bộ, microservices.
- **RabbitMQ**: Message queue truyền thống, dễ tích hợp.

## Triển khai & Vận hành

- **Docker**: Đóng gói ứng dụng thành container.
- **Kubernetes**: Quản lý và triển khai ứng dụng phân tán.
- **Prometheus**: Thu thập metrics từ ứng dụng, container, hệ thống.
- **Grafana**: Trực quan hóa metrics từ Prometheus, tạo dashboard giám sát.
- **ELK / OpenSearch**: Quản lý và phân tích log.

## Quản lý mã nguồn & CI/CD

- **Git**: Quản lý source code.
- **GitHub**: Lưu trữ và tích hợp CI/CD.
- **GitHub Actions**: Tự động hóa build, test, deploy.
- **ArgoCD / FluxCD**: GitOps cho triển khai Kubernetes.

---

## Frontend (Next.js)

**Next.js**: Framework React fullstack.

- **App Router**: Routing hiện đại, hỗ trợ server component, nested layout.
- **Redux**: Quản lý state toàn cục (nếu cần cho các state phức tạp hoặc chia sẻ nhiều component).
- **pnpm / bun**: Trình quản lý package thay thế npm/yarn.
- **TypeScript**: Giúp code an toàn, dễ bảo trì.

### Testing (JS/TS)

- **Jest**: Unit test cho JS/TS.
- **Mocha**: Kiểm thử JS bổ sung.
- **React Testing Library**: Kiểm thử component React.
- **Cypress / Playwright**: End-to-end test cho ứng dụng web
  - Cypress: Dễ dùng, cộng đồng lớn.
  - Playwright: Nhanh hơn, hỗ trợ đa trình duyệt, đa ngôn ngữ.
- **Bundle Analyzer (next-bundle-analyzer)**: Kiểm tra kích thước bundle.

### Triển khai

**Vercel**: Nền tảng triển khai Next.js nhanh chóng, tích hợp CI/CD.
**Docker / Kubernetes**: Triển khai linh hoạt, mở rộng quy mô.
**API Gateway**: Định tuyến request frontend/backend, bảo mật, rate limit, logging (VD: NGINX, Kong, Spring Cloud Gateway).
**Payment Gateway**: Tích hợp thanh toán trực tuyến (Stripe, PayPal, VNPay, MoMo...)

---

## Machine Learning / Deep Learning

- **Python**: Ngôn ngữ chính cho ML/DL.
- **Pixi**: Quản lý môi trường và dependency cho Python.
- **Taskfile (go-task)**: Quản lý task tự động.
- **Abilian DevTools (ADT)**: Bộ công cụ hỗ trợ phát triển Python.
- **Colab Extension (VSCode)**: Tích hợp Google Colab vào VSCode.

### Dependencies & Tools

- **Python**
- **mypy**: Kiểm tra kiểu tĩnh cho Python.
- **bandit**: Phân tích bảo mật mã Python.
- **pip-audit**: Kiểm tra lỗ hổng dependency Python.
- **go-task**: Quản lý task automation.
- **pytest-html**: Xuất báo cáo test HTML.
- **dvc**: Quản lý dữ liệu và version cho ML.
- **dvc-s3**: Tích hợp DVC với S3.
- **abilian-devtools**: Công cụ phát triển Python.
- **clearml (extras: s3)**: Quản lý thí nghiệm ML, tích hợp S3.
- **awscli**: Công cụ dòng lệnh AWS.

---
