# ✅ main.py
from stats.missions_by_user import get_missions_by_user
from stats.tips import get_tips
from stats.results import get_results_distribution
from stats.detailed_internal_missions import get_detailed_internal_missions
from stats.detailed_external_missions import get_detailed_external_missions
from stats.provider_missions import get_provider_missions

from utils import (
    get_date_ranges,
    format_comparative_table,
    create_notion_blocks
)
from notion_utils import send_to_notion
from ai_summary import generate_summary_from_tables

import os
from datetime import datetime

if __name__ == "__main__":
    start, end, start_prev, end_prev = get_date_ranges()

    print(f"\n📅 Current period : {start} → {end}")
    print(f"📅 Last period : {start_prev} → {end_prev}\n")

    blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"📅 Current period: {start} → {end}"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"📅 Previous period: {start_prev} → {end_prev}"}}]
            }
        }
    ]

    # Résumé IA
    #text_summary = "\n\n".join([
        #format_comparative_table(get_detailed_internal_missions()),
        #format_comparative_table(get_detailed_external_missions()),
        #format_comparative_table(get_failed_missions()),
       #format_comparative_table(get_missions_internes()),
        #format_comparative_table(get_missions_externes()),
        #format_comparative_table(get_missions_by_user()),
        #format_comparative_table(get_tips()),
        #format_comparative_table(get_results_distribution())
    #])
    #blocks += generate_summary_from_tables(text_summary)

    # Données complètes
    blocks += create_notion_blocks("📊 Internal Missions", get_detailed_internal_missions())
    blocks += create_notion_blocks("🌐 External Missions", get_detailed_external_missions())
    blocks += create_notion_blocks("👤 Missions by User", get_missions_by_user())
    blocks += create_notion_blocks("💰 Tips", get_tips())
    blocks += create_notion_blocks("📈 Results Distribution", get_results_distribution())
    blocks += create_notion_blocks("📊 Mark as Failed Breakdown", get_provider_missions())

    print("Notion database ID:", os.getenv("NOTION_DATABASE_ID"))

    send_to_notion(
        database_id=os.getenv("NOTION_DATABASE_ID"),
        title=f"Report {datetime.now().strftime('%d %B %Y')}",
        children=blocks
    )

    print("\n✅ Rapport envoyé dans Notion avec succès !")
