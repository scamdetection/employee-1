# Employee Management System - Knowledge Transfer

## 1. Project Overview
The Employee Management System is an enterprise web application used to manage employee information and internal organizational activities. The application is used by employees, managers, HR teams, administrators, and support teams.

## 2. Business Purpose
The system provides a centralized platform for managing employee profiles, departments, attendance, leave requests, project assignments, and employee-related reports.

## 3. Technology Stack
Backend: Java, Spring Boot, Spring MVC, Spring Data JPA, Spring Security.
Frontend: React.js, HTML, CSS, JavaScript, Bootstrap.
Database: MySQL.
Build: Maven.
Version control: Git.
Testing: JUnit, Mockito, Postman.
DevOps: Jenkins, Docker.
Deployment: AWS and Linux.
Monitoring: Application and server monitoring.

## 4. Application Architecture
The application follows a layered architecture:
User -> React Frontend -> REST API -> Controller Layer -> Service Layer -> Repository Layer -> MySQL Database.

## 5. Employee Module
The Employee Module manages Employee ID, employee name, email, phone number, department, designation, joining date, manager, and employee status. Employee statuses include ACTIVE, INACTIVE, ON_NOTICE, and TERMINATED.

## 6. Authentication
Authentication is required before accessing protected application features. Credentials are validated by the backend and an authentication token is generated after successful login.

## 7. Authorization
Role-based authorization determines access. Employees can view their own information, managers can view team information, HR can manage employee records, and administrators can manage application configuration.

## 8. Employee Creation Flow
HR enters employee details, the frontend validates fields, the request is sent to the REST API, the controller receives it, the service validates business rules, the repository saves the employee, and the database stores the record. Duplicate email validation is performed.

## 9. REST APIs
Examples include:
POST /api/auth/login
GET /api/employees
GET /api/employees/{id}
POST /api/employees
PUT /api/employees/{id}
DELETE /api/employees/{id}
GET /api/departments
POST /api/departments
GET /api/leaves
POST /api/leaves
PUT /api/leaves/{id}/approve
PUT /api/leaves/{id}/reject
GET /api/attendance/{employeeId}

## 10. Controller Layer
The controller receives HTTP requests, validates request structure, calls the service layer, and returns responses. Complex business logic should not be placed in controllers.

## 11. Service Layer
The service layer contains business logic such as email uniqueness checks, department validation, manager validation, employee status validation, and leave business rules.

## 12. Repository Layer
The repository communicates with MySQL using Spring Data JPA. Common operations include findById, findAll, findByEmail, findByDepartmentId, save, and delete.

## 13. Database
Important tables include employees, departments, users, roles, attendance, leave_requests, projects, employee_projects, and audit_logs.

## 14. Leave Management
Employees can apply for leave and managers can approve or reject requests. Leave statuses are PENDING, APPROVED, REJECTED, and CANCELLED. The system validates leave balance and request rules.

## 15. Attendance
Attendance stores employee ID, date, login time, logout time, working hours, and attendance status. Statuses can be PRESENT, ABSENT, HALF_DAY, or LEAVE.

## 16. Project Assignment
Employees can be assigned to projects. Project information includes project ID, name, manager, start date, end date, and status. employee_projects maps employees to projects.

## 17. Validation
Frontend validation checks basic input while backend validation performs business validation. Email format, required fields, joining date, department existence, and duplicate email are checked.

## 18. Exception Handling
Common exceptions include EmployeeNotFoundException, DepartmentNotFoundException, DuplicateEmployeeException, InvalidLeaveRequestException, and UnauthorizedException. Centralized exception handling returns controlled error responses.

## 19. Security
Security practices include password hashing, authentication tokens, role-based authorization, HTTPS, input validation, protected API endpoints, token expiration, and secure configuration. Secrets must not be committed to Git.

## 20. Git Workflow
Developers create feature or bug-fix branches, implement changes, run tests, commit, push, create a Pull Request, complete code review and CI checks, and then merge.

## 21. Maven Build
Maven manages dependencies and builds. Common commands are mvn clean, mvn test, mvn package, and mvn clean install. The pom.xml contains project dependencies and build configuration.

## 22. Unit Testing
JUnit and Mockito are used for testing employee creation, employee search, updates, duplicate validation, leave approval, and leave rejection.

## 23. API Testing
Postman is used to test REST APIs. Status codes, response bodies, validation, error handling, and database changes are checked.

## 24. CI/CD Pipeline
Jenkins performs checkout, Maven build, unit tests, code quality checks, packaging, Docker image creation, and deployment. A failed important stage should stop the pipeline.

## 25. Docker
Docker packages the application into images and provides a consistent runtime environment across development, testing, and production.

## 26. AWS Deployment
The application can be deployed on AWS using a load balancer, application server, Docker container, and MySQL database.

## 27. Logging
Logs contain timestamp, log level, service, request ID, user ID, operation, message, and exception information. Passwords and sensitive data must not be logged.

## 28. Production Support
When a production issue occurs, collect the error message, employee ID, request time, API endpoint, environment, request ID, and relevant logs. Reproduce the issue in a lower environment when possible.

## 29. Production Issue Example
If employee records load slowly, check API response time and database queries. If thousands of records are returned at once, introduce pagination such as GET /api/employees?page=0&size=20.

## 30. Database Performance
Check query execution time, indexes, table scans, unnecessary joins, duplicate queries, pagination, and connection pool configuration. Frequently searched fields such as employee_id, email, and department_id may need indexes based on actual query behavior.

## 31. Common Issues
Common issues include login failure, employee API failure, leave approval failure, slow application, database connectivity problems, invalid requests, authentication problems, and deployment failures.

## 32. Deployment Environments
The application moves through Development, QA, Staging, and Production environments. QA performs functional and regression testing, while staging is used for final validation.

## 33. Configuration Management
Environment-specific values such as database URLs, credentials, API URLs, email configuration, and logging configuration should be supplied through secure configuration rather than hardcoded.

## 34. Developer Responsibilities
Daily activities include attending stand-ups, reviewing Jira tickets, understanding requirements, coding, writing unit tests, testing APIs, fixing bugs, reviewing Pull Requests, checking CI results, deploying development changes, supporting QA, and investigating production issues.

## 35. KT Handover
A new developer should understand business requirements, architecture, database, backend structure, APIs, security, testing, Git, CI/CD, deployment, logging, and production troubleshooting.

## 36. Complete Employee Flow
A typical employee creation flow is:
Frontend -> REST API -> Controller -> Service -> Repository -> MySQL.

## 37. Important Business Rules
Duplicate employee emails are not allowed. Protected APIs require authentication. Only authorized roles can manage employee records. Leave requests must follow approval rules. Employee data should be validated before database insertion.

## 38. Troubleshooting Approach
Identify what happened, when it happened, which user was affected, which API was called, which environment was involved, what error occurred, and which request ID is available. Then check logs, database behavior, recent deployments, and dependent services.

## 39. Production Change Process
Production changes should be developed in a branch, reviewed, tested, passed through CI/CD, validated in lower environments, approved, deployed according to the release process, and monitored after deployment.

## 40. Conclusion
The Employee Management System is an enterprise software application built with Java, Spring Boot, React, MySQL, Git, Maven, Jenkins, Docker, and AWS. A new developer should understand the business flow, architecture, database, REST APIs, security, testing, CI/CD, deployment, logging, and production troubleshooting.
