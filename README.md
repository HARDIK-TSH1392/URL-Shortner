
# URL Shortener Service

This project implements a simplified URL shortener service using Python and Flask, similar to services like Bitly. It provides functionality to shorten long URLs, redirect users to the original URLs, and track access statistics.

---

## **Features**
1. **URL Shortening**: Converts a long URL into a shorter, unique URL.
2. **Redirection**: Redirects from the shortened URL to the original URL.
3. **Access Statistics**: Tracks how many times a shortened URL has been accessed.
4. **Time-to-Live (TTL)**: Optionally expires shortened URLs after a specified duration.
5. **Error Handling**: Handles invalid URLs, expired links, and non-existent shortened URLs gracefully.
6. **Extensible Design**: Modular and scalable to support additional features in the future.

---

## **Approach**

### **1. High-Level Design**
- **URL Shortener Class**:
  - Handles core functionalities such as generating short URLs, storing mappings, validating URLs, and tracking statistics.
  - Uses in-memory storage (Python dictionaries) for mapping short URLs to their corresponding long URLs, along with metadata like access counts and expiration times.

- **Flask API**:
  - Provides RESTful endpoints for interacting with the URL shortener:
    - `/shorten`: Shortens a long URL.
    - `/<short_url_key>`: Redirects to the original URL.
    - `/stats/<short_url_key>`: Fetches access statistics for a short URL.

### **2. Design Decisions**
- **Hashing for Short URL Keys**:
  - Used MD5 hashing to generate 8-character unique keys for shortened URLs. This ensures uniqueness and consistency without storing unnecessary data.
- **Thread Safety**:
  - Included `threading.Lock` to ensure thread-safe operations on in-memory data structures.
- **TTL Support**:
  - Implemented expiration functionality by associating timestamps with each URL and checking validity on each access.
- **Validation**:
  - Ensured that URLs are validated for both structure (using `urlparse`) and reachability (using a lightweight `HEAD` request).

---

## **Challenges Faced**

1. **Concurrency Management**:
   - Handling multiple simultaneous requests required ensuring thread safety when modifying shared data structures.
   - **Resolution**: Used Python's `threading.Lock` to manage concurrent access.

2. **TTL Functionality**:
   - Ensuring efficient expiration checks without degrading performance.
   - **Resolution**: Implemented expiration checks only during redirection or access, avoiding background tasks for cleanup.

3. **Short URL Accessibility**:
   - Initially, shortened URLs did not work because they weren't backed by a functional server.
   - **Resolution**: Integrated Flask to handle HTTP requests and make the service accessible via a local web server.

---

## **Endpoints**
1. **POST `/shorten`**
   - **Request**:
     ```json
     {
       "long_url": "https://example.com",
       "ttl": 3600
     }
     ```
   - **Response**:
     ```json
     {
       "short_url": "http://localhost:5000/abc12345"
     }
     ```

2. **GET `/<short_url_key>`**
   - Redirects to the original URL associated with the short key.

3. **GET `/stats/<short_url_key>`**
   - **Response**:
     ```json
     {
       "access_count": 5
     }
     ```

---

## **How to Run the Project**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/url-shortener.git
   cd url-shortener
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Start the Flask application:
   ```bash
   python app.py
   ```

4. Use Postman, cURL, or your browser to test the endpoints.

