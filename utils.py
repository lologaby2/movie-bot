import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_and_rewrite(english_text: str) -> str:
    """يترجم النص من الإنجليزية إلى العربية ويعيد صياغته بطريقة احترافية تصلح لفيديو قصير."""
    system_prompt = """
أنت كاتب محترف في تلخيص الأفلام. مهمتك هي ترجمة النص التالي من الإنجليزية إلى العربية، 
ثم إعادة صياغته بأسلوب جذاب ومختصر ومناسب لفيديو قصير، بدون حرق الأحداث.
يجب أن يكون الأسلوب مشوقًا وجاذبًا، وتُستخدم اللغة العربية الفصحى البسيطة.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": english_text.strip()}
            ],
            temperature=0.8,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ حدث خطأ في الترجمة: {e}"
