# Auction Plaza API Documentation

## User Registration

**Description:** Register a new user.

- **Method:** POST
- **URL:** http://127.0.0.1:8000/api/v1/users/register
- **Body:**
  ```json
  {
      "email": "chetan@gmail.com",
      "first_name": "cheten",
      "last_name": "ghhdawaje",
      "password": "123456789"
  }
  
---

## User Login

**Description:** Log in with user credentials.

- **Method:** POST
- **URL:** http://127.0.0.1:8000/api/v1/users/login
- **Body:**
  ```json
  {
      "email": "chetan@gmail.com",
      "password": "123456789"
  }

---

## Retrieve Bids

**Description:** Retrieve bids for a specific product.

- **Method:** GET
- **URL:** http://127.0.0.1:8000/api/v1/bids/

---

## Create Bid

**Description:** Create a new bid for a product.

- **Method:** POST
- **URL:** http://127.0.0.1:8000/api/v1/bids/
- **Body:**
  ```json
  {
      "product": 1,
      "bidder": 1,
      "bid_amount": 99
  }
  
---

## Apply for Bid

**Description:** Apply for a bid on a product.

- **Method:** POST
- **URL:** http://127.0.0.1:8000/api/v1/bids/apply
- **Body:**
  ```json
  {
      "user": 1,
      "product": 1
  }
  
---

## Bid Apply

**Description:** Apply for bidding on a product.

- **Method:** GET
- **URL:** http://127.0.0.1:8000/api/v1/bids/apply
- **Headers:** 
  - Authorization: {{token}}

---