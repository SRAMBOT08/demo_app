# QuickCourt Frontend

Sports Facility Booking Platform - React Frontend

## Features

- **User Dashboard**: Search and book sports facilities
- **Owner Dashboard**: Manage facilities and view earnings
- **Admin Panel**: Approve facilities and manage users
- **Match-Making**: Join or create public matches
- **Reviews & Ratings**: Rate and review facilities
- **Real-time Analytics**: Charts and insights

## Tech Stack

- React 18
- React Router v6
- Tailwind CSS
- Chart.js
- Axios
- JWT Authentication

## Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm start
```

Runs on [http://localhost:3000](http://localhost:3000)

### Build

```bash
npm build
```

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/     # Reusable components
│   ├── pages/          # Page components
│   ├── context/        # React Context (Auth)
│   ├── services/       # API services
│   ├── utils/          # Helper functions
│   ├── hooks/          # Custom hooks
│   ├── App.js
│   └── index.js
```

## API Configuration

Update `src/services/api.js` with your backend URL:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

## Role-Based Access

- **User**: Browse, book, join matches
- **Owner**: Manage facilities, view earnings
- **Admin**: Approve facilities, manage users
