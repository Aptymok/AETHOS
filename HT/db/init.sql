CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT,
  role TEXT DEFAULT 'testigo',
  coherence FLOAT DEFAULT 0.5,
  style TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE cards (
  id SERIAL PRIMARY KEY,
  title TEXT,
  path TEXT,
  frequency TEXT,
  principle TEXT,
  protocol TEXT,
  inverted_protocol TEXT,
  image_url TEXT
);

CREATE TABLE manifestations (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  intention TEXT,
  mask TEXT,
  entropy FLOAT,
  alignment FLOAT,
  keywords TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE diagnostics (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  query JSONB,
  result JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
