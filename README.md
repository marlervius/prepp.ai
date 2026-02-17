# Prepp.ai - Lærerens trygge havn

En SaaS-plattform som gir lærere i norsk skole kvalitetssikret, kildebelagt fagbriefing på sekunder ved hjelp av AI og Retrieval-Augmented Generation (RAG).

## 🚀 Funksjoner

- **Strukturerte lærermanualer**: Få komplette undervisningsbriefer med LK20-kobling, faglig dybde, pedagogiske tips og elevspørsmål
- **Kildebelagt innhold**: Basert på verifiserte norske kilder (SNL, NDLA, Udir)
- **AI-drevet**: Bruker Claude Sonnet for høykvalitets, kontekstbevisst generering
- **RAG-arkitektur**: Retrieval-Augmented Generation sikrer faktabasert innhold
- **Responsivt design**: Fungerer på desktop og mobil

## 🏗️ Teknisk arkitektur

### Frontend
- **Next.js 14+** med App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling

### Backend
- **FastAPI** (Python) for API
- **Supabase** (PostgreSQL + pgvector) for database og autentisering
- **Redis** for caching
- **Claude/Anthropic** for AI-generering

### AI Pipeline
- **Single-agent arkitektur** (MVP) med strukturert prompt
- **RAG** mot norske kilder
- **pgvector** for vektorsøk

## 🛠️ Installasjon og oppsett

### Forutsetninger
- Node.js 18+
- Python 3.11+
- Supabase konto
- Anthropic API nøkkel

### 1. Klone repository
```bash
git clone <repository-url>
cd prepp.ai
```

### 2. Oppsett av backend
```bash
cd prepp-ai-backend

# Installer Python dependencies
pip install -r requirements.txt

# Kopier environment fil
cp .env.example .env

# Rediger .env med dine API-nøkler
nano .env
```

### 3. Oppsett av database
```bash
# Installer Supabase CLI
npm install -g supabase

# Initialiser Supabase prosjekt
cd prepp-ai-app
supabase init

# Kjør database migreringer
supabase db push
```

### 4. Oppsett av frontend
```bash
cd prepp-ai-app

# Installer dependencies
npm install

# Start utviklingsserver
npm run dev
```

### 5. Start backend
```bash
cd prepp-ai-backend

# Start FastAPI server
python -m app.main
```

## 🔧 Konfigurasjon

### Environment variabler

Backend (`.env`):
```env
# Database
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
DATABASE_URL=your-postgres-connection-string

# AI
ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key

# Caching
REDIS_URL=redis://localhost:6379

# External APIs
SNL_API_KEY=your-snl-api-key
```

Frontend (`.env.local`):
```env
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## 🚦 Bruk

1. Åpne http://localhost:3000
2. Velg fag fra dropdown (LK20-fag)
3. Velg trinn (1-13 eller VG1-VG3)
4. Skriv inn tema
5. Klikk "Generer lærermanual"
6. Få en komplett undervisningsbrief på sekunder

## 📊 API Endepunkter

### POST /api/v1/briefs
Generer en ny undervisningsbrief.

**Request:**
```json
{
  "subject": "Naturfag",
  "grade": "8",
  "topic": "fotosyntese"
}
```

**Response:**
```json
{
  "id": "uuid",
  "subject": "Naturfag",
  "grade": "8",
  "topic": "fotosyntese",
  "content": {
    "lk20_kobling": "...",
    "faglig_dybde": "...",
    "pedagogiske_tips": "...",
    "elev_sporsmal_feller": "...",
    "kilder": "..."
  },
  "sources": [...],
  "processing_time_ms": 2450
}
```

## 🧪 Testing

```bash
# Backend tester
cd prepp-ai-backend
pytest

# Frontend tester
cd prepp-ai-app
npm test
```

## 📈 Veikart

### MVP (Gjeldende)
- ✅ Webapplikasjon med grunnleggende funksjonalitet
- ✅ AI-genererte briefer med RAG
- ✅ Enkel brukerregistrering
- ✅ Caching av identiske spørringer

### V1.0 (Neste)
- PDF-eksport
- Historikk og lagring
- Betalingsintegrasjon (Stripe)
- "Grav dypere" oppfølgingsfunksjon

### V2.0 (Framtidig)
- Multi-agent arkitektur
- Mobilapp med flashcards
- Feide SSO-integrasjon
- Skolelisenser

## 🤝 Bidrag

Vi setter pris på bidrag! Se CONTRIBUTING.md for retningslinjer.

## 📄 Lisens

Dette prosjektet er lisensiert under MIT License.

## 📞 Kontakt

For spørsmål eller samarbeid, kontakt oss på kontakt@prepp.ai