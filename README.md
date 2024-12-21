
# Ecoomerce Chat-Bot
The E-commerce Sales Chatbot is designed to enhance customer experience on e-commerce platforms by enabling efficient product search, exploration, and purchase processes. It integrates a responsive frontend, an API-driven backend, and a relational database to provide seamless and interactive functionality for users.
## Features
1) User Authentication:



2) Product Search:


3) Cart Management:

4) Chat Functionality:

5) Scalable Backend:



## Tech Stack

**Frontend**:

1)React (for building the user interface)

2)Tailwind CSS (for styling)

3)Clerk Authentication

**Backend**:
1)Flask (API development)

2)SQLAlchemy (ORM for database interaction)

**Database**:
1)MYSQL (relational database for storing user, product, cart, and chat data)

**Tools**:
1)ChatGPT for mock data Generation
## Installation

1)Install my-project with npm

```bash
  npm install my-project
  cd my-project
```
2)Install frontend dependencies:

```bash
  cd frontend
  npm install 
``` 
3)Install backend dependencies:

```bash
  cd ../backend
  pip install -r requirements.txt
```
4)Set up the database:

i) Create a PostgreSQL database named ecommerce_chatbot.

ii) Update the database connection string in config.py.

iii) Populate the database

5) start the backend server

```bash
  python route.py
```

6) start the frontend development server
```bash
  cd ../frontend
  npm start
```
## API Reference

#### Authentication

```http
  POST/auth
```

| Parameter | Type     |
| :-------- | :------- | 
| `email` | `string` | 
| `name` | `string`|

#### Get products

```http
  GET /get-product?category=category&max_price=max_price&min_price=min_price&instock=instock&brand=brand&name=name&rating=rating&limit=limit
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `category`      | `string` | **Required**. category of item to fetch |
| `max_price`      | `string` | **Required**. max_price of item to fetch |
| `min_price`      | `string` | **Required**. min_price of item to fetch |
| `instock`      | `string` | **Required**. instock of item to fetch |
| `brand`      | `string` | **Required**. brand of item to fetch |
| `name`      | `string` | **Required**. name of item to fetch |
| `rating`      | `string` | **Required**. rating of item to fetch |
| `limit`      | `string` | **Required**. limit of item to fetch |


#### Get a product
```http
  GET/get-a-product/id
```
|Parameter|tpye|Description|
|:--------|:---|:----------|
|`id`|`integer`|**Required**. id of the product|

#### Save a chat
```http
  POST /save-chat
```
|Parameter|tpye|Description|
|:--------|:---|:----------|
|`email`|`String`|**Required**. Email of the user whose chat is being retrieved.|


##Get a cart
```http
  GET /cart
```
|Parameter|tpye|Description|
|:--------|:---|:----------|
|`email`|`String`|**Required**. Email of the user whose cart is being retrieved.|


##Add to  cart
```http
  POST /add-to-cart
```
|Parameter|tpye|Description|
|:--------|:---|:----------|
|`email`|`String`|**Required**. Email of the user whose cart is being retrieved.|
|`product`|`String`|**Required**. Product to be added.|
|`quantity`|`Integer`|**Required**. quantity of the product .|



## Key Learnings
**1) Frontend**:
Leveraged React’s component-based architecture for scalability.

Implemented responsive design for mobile and desktop views.

**2) Backend**:
Optimized SQLAlchemy queries for dynamic filtering.

Designed modular and reusable API endpoints.

**3) Database Management**:
Gained hands-on experience in schema design and mock data generation.

**4) Generative AI and Large language Models**:
Used a generative AI model to dynamically generate chatbot responses, enhancing user interaction and experience.

**5) LLMs Integration**:
Incorporated large language models (LLMs) to refine chatbot responses and improve context understanding, providing more accurate and helpful user interactions.
## Presentation Details

**1) Project Approach**:
Developed a chatbot capable of assisting users throughout the e-commerce process.

Integrated frontend, backend, and database components seamlessly.

**2) Technology Utilized**:
React, Flask, MySQL, Clerk Authentication.

**3) Key Learning**:
Modular development, database optimization, effective API handling, leveraging generative AI, and incorporating LLMs for enhanced chatbot functionality.