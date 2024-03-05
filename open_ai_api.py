from openai import OpenAI
client = OpenAI(api_key='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')

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": '''Summarize the given doc:
     The Flutter project expects Flutter's contributors to act professionally
    and respectfully. Flutter contributors are expected to maintain the safety
    and dignity of Flutter's social environments (such as GitHub and Discord).

    Specifically:

    * Respect people, their identities, their culture, and their work.
    * Be kind. Be courteous. Be welcoming.
    * Listen. Consider and acknowledge people's points before responding.

    Should you experience anything that makes you feel unwelcome in Flutter's
    community, please contact [conduct@flutter.dev](mailto:conduct@flutter.dev)
    or, if you prefer, directly contact someone on the project, for instance
    [Hixie](mailto:ian@hixie.ch).

    The Flutter project will not tolerate harassment in Flutter's
    community, even outside of Flutter's public communication channels.

        '''},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)