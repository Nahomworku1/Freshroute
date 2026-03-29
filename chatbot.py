from flask import Flask, request
import os
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)

# ── PASTE YOUR KEY HERE ───────────────────────────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
# ─────────────────────────────────────────────────────────────

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are FreshRoute AI — a post-harvest intelligence assistant for smallholder farmers in Ethiopia and the Global South.

When a farmer messages you, ALWAYS respond in this exact format:

⚠️ SPOILAGE ALERT
[1 sentence: how many hours they have and the main risk factor]

📊 YOUR SITUATION
• Crop: [what they mentioned]
• Risk level: [Critical / High / Moderate / Low]
• Main threat: [temperature or humidity]

🏪 BEST BUYER MATCH
[Buyer name] — [distance]km away
Price: ETB [price]/kg
Estimated revenue: ETB [quantity × price]

🗺️ ACTION
[1 specific sentence — sell today, use cold storage, or take alternate route]

💡 IF YOU ACT NOW
Waste: [X]% → Save ETB [amount]
FreshRoute fee: ETB [1.5% of revenue]

Rules:
- NEVER ask for clarification. Always give a full response.
- If anything is missing, assume reasonable defaults: 100kg, Addis Ababa region, open air storage.
- Realistic ETB prices: tomatoes 15-22, mangoes 8-15, maize 7-10, bananas 6-12, leafy greens 5-10, coffee cherries 28-42, papaya 8-14
- Main buyers near Addis Ababa: Addis Ababa Produce Market (28km), Bishoftu Cold Hub (45km)
- Main buyers near Jimma: Jimma Coffee Cooperative (8km), Jimma Central Market (5km)
- Main buyers near Dire Dawa: Dire Dawa Central Market (5km), Harar Cold Storage (52km)
- Keep response under 200 words
- CRITICAL: Always respond in the SAME language the farmer used.
  If they write in English → respond in English
  If they write in Amharic → respond in Amharic
  If they write in French → respond in French
  If they write in any other language → respond in that same language
"""

CONTEXT_TEMPLATE = """
Farmer message: {message}

Current conditions (Ethiopia):
- Temperature: 28°C (above average — accelerates spoilage)
- Humidity: 72% (moderate-high — increases fungal risk)
- Addis-Nazret road: flooded, adds 2 hours to eastern route
- Western ring road: clear and safe
"""

conversation_history = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "unknown")
    print(f"\n📱 {sender}: {incoming_msg}")

    if sender not in conversation_history:
        conversation_history[sender] = []

    conversation_history[sender].append({
        "role": "user",
        "content": CONTEXT_TEMPLATE.format(message=incoming_msg)
    })

    history = conversation_history[sender][-6:]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *history],
            max_tokens=400,
            temperature=0.4,
        )
        reply = response.choices[0].message.content.strip()
        conversation_history[sender].append({"role": "assistant", "content": reply})
        print(f"🤖 FreshRoute:\n{reply}\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        reply = (
            "⚠️ FreshRoute is temporarily unavailable.\n"
            "Please try again in a moment.\n\n"
            "For urgent help, text your crop name and quantity — e.g. 'tomatoes 200kg Addis Ababa'"
        )

    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

@app.route("/", methods=["GET"])
def health():
    return """
    <html><body style="font-family:sans-serif;padding:40px;background:#1A1A0A;color:#FAF6EE">
        <h2 style="color:#FCDD09">🌿 FreshRoute WhatsApp Bot 🇪🇹</h2>
        <p style="color:#4BBF7A">✅ Server is running</p>
        <p style="color:#9A9A6E">Webhook: <code style="color:#FAF6EE">/whatsapp</code></p>
        <p style="color:#9A9A6E">Language: Auto-detect — responds in farmer's language</p>
    </body></html>
    """

if __name__ == "__main__":
    print("\n🌿 FreshRoute Ethiopia WhatsApp Bot starting...")
    print("🇪🇹 Auto-detects language — English, Amharic, French and more")
    print("📡 Webhook: http://localhost:5000/whatsapp\n")
    app.run(debug=False, port=5000)