-- Enable pgvector extension for vector embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable Row Level Security
ALTER DATABASE postgres SET "app.jwt_secret" TO 'your-secret-key';

-- Schools table for organizational licenses
CREATE TABLE schools (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    municipality TEXT,
    license_type TEXT DEFAULT 'free' CHECK (license_type IN ('free', 'premium', 'enterprise')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- LK20 goals table - structured Norwegian curriculum data
CREATE TABLE lk20_goals (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    subject TEXT NOT NULL,
    grade TEXT NOT NULL, -- 1-13, VG1-VG3
    goal_text TEXT NOT NULL,
    keywords TEXT[], -- For search indexing
    embedding vector(1536), -- OpenAI text-embedding-ada-002 dimension
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Source chunks table - RAG vector database
CREATE TABLE source_chunks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    source TEXT NOT NULL, -- 'snl', 'ndla', 'udir'
    url TEXT NOT NULL,
    title TEXT,
    content TEXT NOT NULL,
    embedding vector(1536), -- OpenAI text-embedding-ada-002 dimension
    metadata JSONB DEFAULT '{}', -- Additional metadata (subject, grade, last_updated, etc.)
    chunk_index INTEGER, -- Order within document
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Briefs table - generated teaching briefs
CREATE TABLE briefs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    subject TEXT NOT NULL,
    grade TEXT NOT NULL,
    topic TEXT NOT NULL,
    content JSONB NOT NULL, -- Structured brief content
    sources JSONB DEFAULT '[]', -- Array of source references
    tokens_used INTEGER DEFAULT 0,
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Usage logs for analytics and billing
CREATE TABLE usage_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    action TEXT NOT NULL, -- 'brief_generated', 'brief_viewed', etc.
    subject TEXT,
    grade TEXT,
    topic TEXT,
    tokens_used INTEGER DEFAULT 0,
    cost_cents INTEGER DEFAULT 0, -- Cost in cents
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User profiles extension
CREATE TABLE profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT,
    full_name TEXT,
    role TEXT DEFAULT 'teacher' CHECK (role IN ('teacher', 'admin', 'school_admin')),
    school_id UUID REFERENCES schools(id),
    plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'trial', 'pro', 'school')),
    briefs_used INTEGER DEFAULT 0,
    briefs_limit INTEGER DEFAULT 10, -- Trial limit
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_lk20_goals_subject_grade ON lk20_goals(subject, grade);
CREATE INDEX idx_source_chunks_source ON source_chunks(source);
CREATE INDEX idx_source_chunks_metadata ON source_chunks USING GIN(metadata);
CREATE INDEX idx_briefs_user_created ON briefs(user_id, created_at DESC);
CREATE INDEX idx_briefs_subject_grade ON briefs(subject, grade);
CREATE INDEX idx_usage_logs_user_created ON usage_logs(user_id, created_at DESC);

-- Vector indexes for semantic search
CREATE INDEX idx_lk20_goals_embedding ON lk20_goals USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_source_chunks_embedding ON source_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Row Level Security policies
ALTER TABLE schools ENABLE ROW LEVEL SECURITY;
ALTER TABLE lk20_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE source_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE briefs ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);

-- Briefs policies (user_id is nullable for anonymous usage)
CREATE POLICY "Users can view own briefs" ON briefs FOR SELECT USING (auth.uid() = user_id OR user_id IS NULL);
CREATE POLICY "Users can create briefs" ON briefs FOR INSERT WITH CHECK (auth.uid() = user_id OR user_id IS NULL);

-- Schools policies (public read for license validation)
CREATE POLICY "Schools are publicly readable" ON schools FOR SELECT USING (true);

-- LK20 goals policies (public read)
CREATE POLICY "LK20 goals are publicly readable" ON lk20_goals FOR SELECT USING (true);

-- Source chunks policies (public read for RAG)
CREATE POLICY "Source chunks are publicly readable" ON source_chunks FOR SELECT USING (true);

-- Usage logs policies (admin only for inserts, users can view their own)
CREATE POLICY "Users can view own usage" ON usage_logs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "System can insert usage logs" ON usage_logs FOR INSERT WITH CHECK (true);

-- Functions for updating updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_schools_updated_at BEFORE UPDATE ON schools FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();