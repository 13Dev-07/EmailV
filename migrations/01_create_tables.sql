-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID REFERENCES auth.users PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create API keys table
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    key_hash TEXT NOT NULL,
    name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,
    revoked BOOLEAN DEFAULT FALSE,
    UNIQUE(key_hash)
);

-- Create validation results table
CREATE TABLE IF NOT EXISTS validation_results (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email TEXT NOT NULL,
    results JSONB NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create usage quotas table
CREATE TABLE IF NOT EXISTS usage_quotas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    monthly_limit INTEGER NOT NULL DEFAULT 1000,
    current_usage INTEGER NOT NULL DEFAULT 0,
    reset_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Create audit logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    action TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);