# Library Automation System (Flask • MongoDB • Kafka)

## Overview
This project is a **backend Library Automation System (LAS)** designed using a modern, scalable architecture.

It provides RESTful services for managing books, users, borrowing, reservations, and authentication, while leveraging **event-driven communication** via Apache Kafka.

The system was developed as part of an **Advanced Python Programming** course and is structured to reflect **real-world backend engineering practices**.

---

## Core Features

### Backend API
- RESTful API built with **Flask**
- Modular routing and clean separation of concerns

### Database
- **MongoDB** for:
  - Users
  - Books
  - Borrowing records
  - Reservations
  - Fines

### Authentication & Authorization
- **JWT-based authentication**
- Role-based access control:
  - Students
  - Faculty
  - Staff
  - Graduates
- Secure request validation on all protected endpoints

### Messaging & Event Handling
- **Apache Kafka** integration
- Producer–consumer pattern for:
  - Asynchronous events
  - Decoupled system components
  - Scalable message processing

### Testing
- Unit tests for authentication and critical logic
- Focus on correctness and reliability

---

## Project Structure
├── app/ # Application modules / blueprints
├── app.py # Flask app initialization
├── run.py # Application entry point
├── routes.py # API routes
├── models.py # MongoDB models
├── auth.py # JWT authentication logic
├── user.py # User-related operations
├── book.py # Book management logic
├── las.py # Core system logic
├── producer.py # Kafka producer
├── consumer.py # Kafka consumer
├── test_auth.py # Authentication tests
├── README.md



---

## Technologies Used
- Python
- Flask
- MongoDB
- Apache Kafka
- JWT (JSON Web Tokens)
- REST API Design
- Event-Driven Architecture

---

## How to Run

> This repository contains **application logic only**.

### Basic steps:
1. Install dependencies
2. Configure MongoDB connection
3. Start Kafka (Zookeeper + Broker)
4. Run the Flask application

Example:
```bash
python run.py
