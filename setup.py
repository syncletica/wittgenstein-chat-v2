#!/usr/bin/env python3
"""
Setup script for the Wittgenstein Chatbot.
Automates the initial setup process including data creation and indexing.
"""

import os
import sys
from loaders.ingest import DataIngester
from config import Config


def main():
    """Run the complete setup process."""
    print("=" * 60)
    print("WITTGENSTEIN CHATBOT SETUP")
    print("=" * 60)

    # Check if OpenAI API key is set
    if not Config.OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY environment variable is required.")
        print("\nPlease set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print("Or create a .env file with: OPENAI_API_KEY=your-api-key-here")
        return False

    print("✅ OpenAI API key found")

    try:
        # Create data ingester
        ingester = DataIngester()

        # Create sample data
        print("\n📝 Creating sample data...")
        ingester.create_sample_data()
        print("✅ Sample data created successfully")

        # Ingest all data
        print("\n🔍 Ingesting and indexing data...")
        ingester.ingest_all()
        print("✅ Data ingestion complete")

        # Verify indexes were created
        print("\n🔍 Verifying indexes...")
        index_paths = [
            Config.AUTHORED_INDEX_PATH,
            Config.DESCRIPTIVE_INDEX_PATH,
            Config.EXTERNAL_INDEX_PATH,
        ]

        all_created = True
        for path in index_paths:
            if os.path.exists(f"{path}.faiss") and os.path.exists(
                f"{path}_metadata.json"
            ):
                print(f"✅ {os.path.basename(path)} index created")
            else:
                print(f"❌ {os.path.basename(path)} index missing")
                all_created = False

        if all_created:
            print("\n🎉 Setup completed successfully!")
            print("\nYou can now run the chatbot with:")
            print("python main.py")
        else:
            print("\n⚠️  Setup completed with warnings. Some indexes may be missing.")
            print(
                "You can still try running the chatbot, but some features may not work."
            )

        return True

    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        print("Please check your configuration and try again.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
