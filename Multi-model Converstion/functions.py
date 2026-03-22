from prompts import groq_prompt, gemini_prompt

def call_groq(groq_msg, gemini_msg,groq_llm):
  msg = [{"role":"system", "content" : groq_prompt}]
  for groq,gemini in zip(groq_msg,gemini_msg):
    msg.append({"role":"assistant", "content" : groq})
    msg.append({"role":"user", "content" : gemini})
  res = groq_llm.invoke(msg)
  return res.content

def call_gemini(groq_msg, gemini_msg, gemini_llm):
  msg = [{"role":"system", "content" : gemini_prompt}]
  for groq,gemini in zip(groq_msg,gemini_msg):
    msg.append({"role":"user", "content" : groq})
    msg.append({"role":"assistant", "content" : gemini})
  msg.append({"role": "user", "content": gemini_msg[-1]})
  res = gemini_llm.invoke(msg)
  return res.text