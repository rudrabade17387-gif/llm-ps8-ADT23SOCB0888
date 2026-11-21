
import os
import re
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "models/gemini-3.8-flash"

st.set_page_config(
    page_title="Product Description Writer",
    page_icon="🛍️",
    layout="centered"
)


def count_words(text):
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", text))


def extract_result(text):

    title_match = re.search(
        r"TITLE:\s*(.*?)\s*BENEFIT 1:",
        text,
        re.IGNORECASE | re.DOTALL
    )

    benefit_matches = re.findall(
        r"BENEFIT ([123]):\s*(.*?)(?=\s*BENEFIT [123]:|\s*DESCRIPTION:)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    description_match = re.search(
        r"DESCRIPTION:\s*(.*?)\s*END_DESCRIPTION",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if not title_match or not description_match:
        raise ValueError("Gemini returned an unexpected output format.")

    # Ensure exactly three benefits in the correct order
    if [number for number, _ in benefit_matches] != ["1", "2", "3"]:
        raise ValueError("Gemini did not return exactly three benefits.")

    title = title_match.group(1).strip()

    benefits = [
        benefit.strip().lstrip("-•* ").strip()
        for _, benefit in benefit_matches
    ]

    description = description_match.group(1).strip()

    if not title or not all(benefits) or not description:
        raise ValueError("Some generated fields are empty.")

    words = count_words(description)

    if words != 60:
        raise ValueError(
            f"Description contains {words} words instead of 60. "
            "Please try again."
        )

    return {
        "title": title,
        "benefits": benefits,
        "description": description
    }


def generate_description(name, features, audience):

    if not API_KEY:
        raise ValueError("Gemini API key not found. Check your .env file.")

    prompt = f"""
You are a professional e-commerce product copywriter.

Product Name: {name}
Product Features: {features}
Target Audience: {audience}

Create a professional product listing.

Follow this EXACT output format.
Do not use JSON or Markdown code fences.

TITLE: Write one attractive product title.
BENEFIT 1: Write the first benefit.
BENEFIT 2: Write the second benefit.
BENEFIT 3: Write the third benefit.
DESCRIPTION:
Write exactly 60 words here.
END_DESCRIPTION

IMPORTANT:
- Exactly three benefits.
- Description must contain exactly 60 words.
- Never invent product features.
- Use simple, persuasive language.
- Focus on the target audience.
- Do not add extra sections or explanations.
"""

    client = genai.Client(api_key=API_KEY)

    try:
        response = client.interactions.create(
            model=MODEL_NAME,
            input=prompt,
            generation_config={
                "max_output_tokens": 1500,
                "thinking_level": "low"
            }
        )

        output_text = response.output_text

        if not output_text:
            raise ValueError("Gemini returned an empty response.")

        return extract_result(output_text)

    finally:
        client.close()


# Main application
st.title("🛍️ Product Description Writer")

st.write(
    "Generate attractive and professional product descriptions "
    "for your online store using AI."
)

st.divider()

with st.form("product_form"):

    st.subheader("Enter Product Details")

    product_name = st.text_input(
        "Product Name",
        placeholder="Example: Wireless Headphones"
    )

    features = st.text_area(
        "Product Features",
        placeholder="Bluetooth 5.3, noise cancellation, 30-hour battery"
    )

    audience = st.text_input(
        "Target Audience",
        placeholder="College students and professionals"
    )

    generate = st.form_submit_button(
        "✨ Generate Product Description",
        use_container_width=True
    )


if generate:

    if not product_name.strip() or not features.strip() or not audience.strip():

        st.warning("Please fill in all three fields.")

    elif not API_KEY:

        st.error("Gemini API key not found. Check your .env file.")

    else:

        try:

            with st.spinner("Generating your product description..."):

                result = generate_description(
                    product_name.strip(),
                    features.strip(),
                    audience.strip()
                )

            st.success("Product description generated successfully!")

            st.divider()

            st.subheader("📝 Generated Product Listing")

            st.markdown("### " + result["title"])

            st.markdown("### ⭐ Key Benefits")

            for benefit in result["benefits"]:
                st.markdown(f"- {benefit}")

            st.markdown("### 📦 Product Description")

            st.write(result["description"])

            st.caption(
                f"Word Count: {count_words(result['description'])}/60"
            )

            output = (
                result["title"]
                + "\n\nKEY BENEFITS\n"
                + "\n".join("- " + benefit for benefit in result["benefits"])
                + "\n\nPRODUCT DESCRIPTION\n"
                + result["description"]
            )

            st.download_button(
                "📥 Download Product Description",
                data=output,
                file_name="product_description.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as error:

            error_message = str(error)

            st.error(f"Generation failed: {error_message}")

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                st.warning(
                    "Gemini free-tier limit reached. Wait for the quota "
                    "to reset before trying again."
                )

            elif "503" in error_message or "UNAVAILABLE" in error_message:
                st.warning(
                    "Gemini service is temporarily unavailable. "
                    "Try again later."
                )

            else:
                st.info("Check the error message before trying again.")
