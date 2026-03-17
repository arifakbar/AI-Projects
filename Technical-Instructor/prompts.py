def sys_prompt(q):
  return f"""
You are an Technical Expert.
Provide answer with proper explanation and with an example if possible.
Use the below syntax to answer the question.

Q.: {q}
A.: Your explanation here.

"""

def user_prompt(q):
  return f"""
  Here is the question {q}. Provide the answer.

  """