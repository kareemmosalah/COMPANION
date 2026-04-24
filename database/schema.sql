-- schema.sql
-- Create database schema and populate with catalog

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    description TEXT,
    image_url TEXT,
    images JSONB DEFAULT '[]'::jsonb,
    available BOOLEAN DEFAULT true,
    features JSONB DEFAULT '[]'::jsonb,
    discount_percentage INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    image_url TEXT
);

-- Note: In PostgreSQL, to truncate and restart identity sequences:
TRUNCATE TABLE products RESTART IDENTITY;

-- Insert all 46 Products based on the complete catalog:

INSERT INTO products (category, name, price, description, image_url, available) VALUES 
('id_holder', 'Scarlet Heart', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/e53e3e/white?text=Scarlet+Heart', true),
('id_holder', 'RTA', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/3182ce/white?text=RTA', true),
('id_holder', 'Arteria', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/e53e3e/white?text=Arteria', true),
('id_holder', 'Lavender Heart', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/805ad5/white?text=Lavender+Heart', true),
('id_holder', 'Lagon RN', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/319795/white?text=Lagon+RN', true),
('id_holder', 'Blue RN', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/3182ce/white?text=Blue+RN', true),
('id_holder', 'Michael Angelo', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/dd6b20/white?text=Michael+Angelo', true),
('id_holder', 'Lagon Heart', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/319795/white?text=Lagon+Heart', true),
('id_holder', 'Lavender RN', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/805ad5/white?text=Lavender+RN', true),
('id_holder', 'Green RN', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/38a169/white?text=Green+RN', true),
('id_holder', 'Parietal Lobe', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/d53f8c/white?text=Parietal+Lobe', true),
('id_holder', 'I''m OK', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/ecc94b/white?text=I''m+OK', true),
('id_holder', 'Brain', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/d53f8c/white?text=Brain', true),
('id_holder', 'Stitch', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/3182ce/white?text=Stitch', true),
('id_holder', 'Qalqas', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/38a169/white?text=Qalqas', true),
('id_holder', 'Stethoscope', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/718096/white?text=Stethoscope', true),
('id_holder', '7abob', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/e53e3e/white?text=7abob', true),
('id_holder', 'Ducktor', 35, 'Cute duck character for pediatrics. Durable clip included.', 'https://placehold.co/400x400/ecc94b/white?text=Ducktor', true),
('id_holder', 'Zazlok', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/4a5568/white?text=Zazlok', true),
('id_holder', 'Pinky', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/ed64a6/white?text=Pinky', true),
('id_holder', 'Shalby', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/319795/white?text=Shalby', true),
('id_holder', 'Boo', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/e53e3e/white?text=Boo', true),
('id_holder', 'Cute', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/ed64a6/white?text=Cute', true),
('id_holder', 'Strong Katkot', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/ecc94b/white?text=Strong+Katkot', true),
('id_holder', 'Katkot', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/ecc94b/white?text=Katkot', true),
('id_holder', 'Heart', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/e53e3e/white?text=Heart', true),
('id_holder', 'Safe Life', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/38a169/white?text=Safe+Life', true),
('id_holder', 'Harry Botter', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/718096/white?text=Harry+Botter', true),
('id_holder', 'Wino', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/d53f8c/white?text=Wino', true),
('id_holder', 'Butterfly', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/805ad5/white?text=Butterfly', true),
('id_holder', 'Vena', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/3182ce/white?text=Vena', true),
('id_holder', 'Original', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/718096/white?text=Original', true),
('id_holder', 'Spider Man', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/e53e3e/white?text=Spider+Man', true),
('id_holder', 'Kuromi', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/1a202c/white?text=Kuromi', true),
('id_holder', 'Iron Man', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/e53e3e/white?text=Iron+Man', true),
('id_holder', 'Captain America', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/3182ce/white?text=Captain+America', true),
('id_holder', 'Hello Kitty', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/ed64a6/white?text=Hello+Kitty', true),
('id_holder', 'Happy', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/ecc94b/white?text=Happy', true),
('id_holder', 'Spider', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/1a202c/white?text=Spider', true),
('id_holder', 'Scary Katkot', 35, 'Fun character ID holder.', 'https://placehold.co/400x400/ecc94b/white?text=Scary+Katkot', true),

('pen_holder', 'Pen Holder', 25, 'Portable black marker in a small size.', 'https://placehold.co/400x400/1a202c/white?text=Pen+Holder', true),

('card', 'Crash Cards', 45, 'Medical question-and-answer reference cards.', 'https://placehold.co/400x400/e53e3e/white?text=Crash+Cards', true),
('card', 'Guidance Cards', 45, 'Reference cards for clinical tools like ISBAR, Glasgow Coma Scale (GCS), vital signs, lab values, and oxygen masks.', 'https://placehold.co/400x400/3182ce/white?text=Guidance+Cards', true),
('card', 'Critical Cards', 45, 'Reference cards for high-acuity situations including burns (Rule of Nines), ECG rhythms, emergency medications, and ABG interpretation.', 'https://placehold.co/400x400/d69e2e/white?text=Critical+Cards', true),

('note', 'Basic Nursing Note', 55, 'A portable, waterproof, 2025 edition pocket guide for nursing basics.', 'https://placehold.co/400x400/38a169/white?text=Nursing+Note', true),
('note', 'Med Term Note', 55, 'A portable pocket guide for anatomy and medical terminology.', 'https://placehold.co/400x400/718096/white?text=Med+Term', true);
