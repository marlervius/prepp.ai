#!/usr/bin/env python3
"""
Script to seed LK20 (Norwegian curriculum) data into the database.
This is essential for the RAG functionality to work properly.
"""

import asyncio
import json
import os
from pathlib import Path
from app.core.database import create_db_connection
from app.services.rag_service import RAGService
from openai import AsyncOpenAI

# Sample LK20 data (simplified for MVP)
LK20_SAMPLE_DATA = [
    {
        "subject": "Norsk",
        "grade": "8",
        "goal_text": "Lytte, lese og se etter informasjon og argumentasjon i tekster fra ulike medier og vurdere tekstens troverdighet",
        "keywords": ["lytte", "lese", "informasjon", "argumentasjon", "troverdighet", "medier"]
    },
    {
        "subject": "Norsk",
        "grade": "8",
        "goal_text": "Skrive ulike typer tekster som er hensiktsmessige for formål og mottaker, og bruke norskfaglige begreper i tekstanalyse",
        "keywords": ["skrive", "tekster", "hensiktsmessige", "mottaker", "begreper", "tekstanalyse"]
    },
    {
        "subject": "Matematikk",
        "grade": "8",
        "goal_text": "Bruke tallinje, koordinatsystem og algebraiske uttrykk til å løse problemer og representere matematiske sammenhenger",
        "keywords": ["tallinje", "koordinatsystem", "algebraiske", "uttrykk", "problemer", "sammenhenger"]
    },
    {
        "subject": "Matematikk",
        "grade": "8",
        "goal_text": "Utforske og generalisere mønstre ved å bruke variable, uttrykk og ligninger, og omforme algebraiske uttrykk",
        "keywords": ["mønstre", "variable", "uttrykk", "ligninger", "omforme", "algebraiske"]
    },
    {
        "subject": "Naturfag",
        "grade": "8",
        "goal_text": "Utforske, forklare og forutsi bevegelser og krefter ved hjelp av Newtons lover og energibegreper",
        "keywords": ["bevegelser", "krefter", "newtons", "lover", "energi", "forklare"]
    },
    {
        "subject": "Naturfag",
        "grade": "8",
        "goal_text": "Undersøke og forklare fotosyntese, respirasjon og stoffkretsløp i naturen",
        "keywords": ["fotosyntese", "respirasjon", "stoffkretsløp", "naturen", "undersøke"]
    },
    {
        "subject": "Engelsk",
        "grade": "8",
        "goal_text": "Forstå hovedinnhold og detaljer i muntlige og skriftlige engelske tekster om kjente temaer",
        "keywords": ["forstå", "hovedinnhold", "detaljer", "muntlige", "skriftlige", "tekster"]
    },
    {
        "subject": "Engelsk",
        "grade": "8",
        "goal_text": "Uttrykke seg muntlig og skriftlig om temaer, hendelser og opplevelser på en sammenhengende måte",
        "keywords": ["uttrykke", "muntlig", "skriftlig", "temaer", "hendelser", "opplevelser"]
    },
    {
        "subject": "Samfunnsfag",
        "grade": "8",
        "goal_text": "Analysere samfunnsstrukturer, maktforhold og demokratiske prosesser i Norge og andre land",
        "keywords": ["analysere", "samfunnsstrukturer", "maktforhold", "demokratiske", "prosesser"]
    },
    {
        "subject": "Historie",
        "grade": "8",
        "goal_text": "Analysere årsaker til og konsekvenser av historiske hendelser, utviklingslinjer og endringsprosesser",
        "keywords": ["analysere", "årsaker", "konsekvenser", "historiske", "hendelser", "utviklingslinjer"]
    }
]

async def seed_lk20_data():
    """Seed LK20 curriculum data into the database"""

    print("🌱 Starting LK20 data seeding...")

    # Initialize services
    db = await create_db_connection()
    openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        for i, goal_data in enumerate(LK20_SAMPLE_DATA):
            print(f"Processing goal {i+1}/{len(LK20_SAMPLE_DATA)}: {goal_data['subject']} {goal_data['grade']}")

            # Create searchable text for embedding
            search_text = f"{goal_data['subject']} {goal_data['grade']} {goal_data['goal_text']} {' '.join(goal_data['keywords'])}"

            # Generate embedding
            embedding_response = await openai.embeddings.create(
                input=search_text,
                model="text-embedding-3-small"
            )
            embedding = embedding_response.data[0].embedding

            # Insert into database
            await db.execute("""
                INSERT INTO lk20_goals (subject, grade, goal_text, keywords, embedding)
                VALUES ($1, $2, $3, $4, $5::vector)
                ON CONFLICT DO NOTHING
            """, goal_data["subject"], goal_data["grade"], goal_data["goal_text"],
                 goal_data["keywords"], embedding)

        print("✅ LK20 data seeding completed!")

    except Exception as e:
        print(f"❌ Error seeding LK20 data: {e}")
        raise
    finally:
        await db.close()

async def seed_sample_source_chunks():
    """Seed some sample source chunks for testing RAG"""

    print("📚 Starting sample source chunks seeding...")

    db = await create_db_connection()
    openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Sample source data
    sample_sources = [
        {
            "source": "snl",
            "url": "https://snl.no/fotosyntese",
            "title": "Fotosyntese",
            "content": "Fotosyntese er den prosessen hvor grønne planter, alger og noen bakterier lager organisk materiale fra uorganiske stoffer ved hjelp av lysenergi. Karbondioksid og vann omdannes til glukose og oksygen. Fotosyntesen foregår i kloroplaster i plantecellene.",
            "subject": "Naturfag",
            "grade": "8"
        },
        {
            "source": "ndla",
            "url": "https://ndla.no/andre-verdenskrig",
            "title": "Andre verdenskrig - årsaker og konsekvenser",
            "content": "Andre verdenskrig (1939-1945) var en global konflikt som involverte de fleste nasjonene i verden. Årsaker inkluderer versaillesfreden etter første verdenskrig, økonomisk depresjon, fremveksten av totalitære regimer som nazismen og fascismen.",
            "subject": "Historie",
            "grade": "8"
        }
    ]

    try:
        for source_data in sample_sources:
            print(f"Processing source: {source_data['title']}")

            # Generate embedding
            embedding_response = await openai.embeddings.create(
                input=source_data["content"],
                model="text-embedding-3-small"
            )
            embedding = embedding_response.data[0].embedding

            # Insert into database
            await db.execute("""
                INSERT INTO source_chunks (source, url, title, content, embedding, metadata)
                VALUES ($1, $2, $3, $4, $5::vector, $6)
                ON CONFLICT DO NOTHING
            """, source_data["source"], source_data["url"], source_data["title"],
                 source_data["content"], embedding,
                 {"subject": source_data["subject"], "grade": source_data["grade"]})

        print("✅ Sample source chunks seeding completed!")

    except Exception as e:
        print(f"❌ Error seeding source chunks: {e}")
        raise
    finally:
        await db.close()

async def main():
    """Main seeding function"""
    print("🚀 Starting database seeding for Prepp.ai")

    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set. Please set it in your environment.")
        return

    if not os.getenv("DATABASE_URL"):
        print("❌ DATABASE_URL not set. Please set it in your environment.")
        return

    try:
        await seed_lk20_data()
        await seed_sample_source_chunks()
        print("🎉 Database seeding completed successfully!")

    except Exception as e:
        print(f"💥 Database seeding failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())