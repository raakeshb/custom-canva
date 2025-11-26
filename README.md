# AI HTML + Tailwind UI Generator (Streamlit + Groq)

Generate complete **HTML + TailwindCSS UI layouts** using natural language prompts.  
The app supports **live preview**, **mobile view toggle**, **manual code editing**, and **HTML download**.

Users only need to enter their **Groq API key** — no installation of models required.

---

## 🚀 Live Features
| Feature | Status |
|--------|-------|
| Convert prompt → UI (HTML + TailwindCSS) | ✅ |
| Modify existing UI using new prompt | ✅ |
| Desktop / Mobile live preview | ✅ |
| Prevent `<a>` navigation inside preview | ✅ |
| Manual HTML editor | ✅ |
| Download UI | ✅ |
| Hidden reasoning (ReAct style) | ✅ |
| Bring-your-own Groq API key | 🔐 |

---

## 🧠 How it Works
1. User enters a UI prompt (e.g., *"Create a pricing page with 3 plans and gradient hero section"*)
2. The Groq model generates HTML + TailwindCSS — no explanations, only UI code
3. The code is rendered live in the preview pane
4. Users can manually edit code or use “Update” to modify via prompt

---

## 🖥 Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend UI | Streamlit |
| LLM Provider | Groq |
| Model | `openai/gpt-oss-safeguard-20b` |
| Styling Framework | TailwindCSS |
| Language | Python |

---

