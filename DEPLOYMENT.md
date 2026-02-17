# 🚀 Prepp.ai Deployment Guide

Denne guiden viser hvordan du deployer Prepp.ai til Render og Vercel.

## 📋 Forutsetninger

- [Render konto](https://render.com) (gratis tier tilgjengelig)
- [Vercel konto](https://vercel.com) (gratis tier tilgjengelig)
- [Google AI Studio API key](https://makersuite.google.com/app/apikey) (gratis)
- [Supabase prosjekt](https://supabase.com) (gratis tier tilgjengelig)

## 🔑 API Keys Setup

### 1. Google Gemini API Key
1. Gå til [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Opprett en ny API key
3. Kopier API key - du trenger denne senere

### 2. Supabase Setup (Valgfritt - for full funksjonalitet)
1. Opprett nytt prosjekt på [Supabase](https://supabase.com)
2. Gå til Settings → API
3. Kopier følgende:
   - Project URL
   - Anon public key
   - Service role key

## 🌐 Deployment til Render (Backend)

### 1. Deploy Backend
1. Gå til [Render Dashboard](https://dashboard.render.com)
2. Klikk "New" → "Web Service"
3. Koble til GitHub repository: `marlervius/prepp.ai`
4. Konfigurer følgende:
   - **Name**: `prepp-ai-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2. Environment Variables for Backend
I Render dashboard, gå til Environment og legg til:

```
GEMINI_API_KEY=din-gemini-api-key-her
SUPABASE_URL=https://din-prosjekt-id.supabase.co (valgfritt)
SUPABASE_ANON_KEY=din-anon-key-her (valgfritt)
SUPABASE_SERVICE_ROLE_KEY=din-service-role-key-her (valgfritt)
DATABASE_URL=postgresql://... (valgfritt)
REDIS_URL=redis://... (valgfritt)
DEBUG=false
LOG_LEVEL=INFO
SECRET_KEY=generer-en-tilfeldig-secret
CORS_ORIGINS=https://din-frontend-url.vercel.app
```

### 3. Deploy
Klikk "Create Web Service" - Render vil bygge og deploye automatisk.

## ⚛️ Deployment til Vercel (Frontend)

### 1. Deploy Frontend
1. Gå til [Vercel Dashboard](https://vercel.com/dashboard)
2. Klikk "Add New..." → "Project"
3. Koble til GitHub repository: `marlervius/prepp.ai`
4. Konfigurer:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `prepp-ai-app`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 2. Environment Variables for Frontend
I Vercel dashboard, gå til Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=https://din-backend-url.onrender.com
```

### 3. Deploy
Klikk "Deploy" - Vercel vil bygge og deploye automatisk.

## 🔗 Koble Frontend og Backend

Etter begge tjenester er deployet:

1. Kopier Render backend URL (f.eks. `https://prepp-ai-backend.onrender.com`)
2. Oppdater Vercel environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://prepp-ai-backend.onrender.com
   ```
3. Redeploy frontend på Vercel

## 🧪 Testing av Deployment

### 1. Test Backend API
```
curl https://din-backend-url.onrender.com/api/v1/health
```

### 2. Test Frontend
Åpne Vercel URL i nettleseren og prøv å generere en lærermanual.

### 3. Test Full Integrasjon
- Velg fag, trinn og tema
- Klikk "Generer lærermanual"
- Sjekk at du får tilbake en strukturert brief

## 💰 Kostnader

- **Render**: Gratis tier (750 timer/måned)
- **Vercel**: Gratis tier (ubegrenset)
- **Google Gemini**: Gratis tier (60 requests/minutt)
- **Supabase**: Gratis tier (500MB database)

## 🔧 Troubleshooting

### Backend Issues
- Sjekk Render logs: Dashboard → Service → Logs
- Verifiser environment variables er satt riktig
- Sjekk at API keys er gyldige

### Frontend Issues
- Sjekk Vercel build logs
- Verifiser NEXT_PUBLIC_API_URL peker til riktig backend
- Sjekk CORS-innstillinger

### API Issues
- Sjekk Gemini API key er gyldig
- Verifiser quota ikke er overskredet
- Sjekk nettverksproblemer

## 📞 Support

Hvis du støter på problemer:
1. Sjekk Render/Vercel dokumentasjon
2. Se GitHub repository issues
3. Kontakt utviklerteamet

---

🎉 **Lykke til med deployment av Prepp.ai!**