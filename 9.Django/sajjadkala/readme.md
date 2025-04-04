

### **How to Run the Project**
1. **Build the Docker image:**
   ```sh
   docker-compose build
   ```
   
2. **Run the containers:**
   ```sh
   docker-compose up -d
   ```

3. **Check logs (optional):**
   ```sh
   docker-compose logs -f
   ```

4. **Access the Django app:**
   Open **`http://localhost:8000`** in your browser.

5. **Stop the containers:**
   ```sh
   docker-compose down
   ```

---

This setup will:
- Run a Django app with PostgreSQL in Docker.
- Use environment variables for database credentials.
- Store PostgreSQL data persistently using Docker volumes.
  
Let me know if you need any modifications! 🚀