"""Per-exercise hints, printed by the hint cell under each exercise."""

exercise_1_1_hint = (
    'The grader checks that the response text contains the characters "1", "2", and "3". '
    "You can usually get Claude to do exactly what you want just by asking plainly."
)

exercise_1_2_hint = (
    'The grader looks for a "TODO" marker. Use the system prompt to make Claude answer '
    "as a terse senior engineer who replies only with a # TODO style code comment."
)

exercise_2_1_hint = (
    'The grader looks for a common Spanish word (e.g. "hola", "gracias"). Tell Claude to '
    "reply in Spanish exactly as you'd ask a teammate: directly and explicitly."
)

exercise_2_2_hint = (
    'The grader checks for the EXACT string "pytest" with no extra words or punctuation. '
    "Ask Claude to reply with only the name, in lowercase, and nothing else."
)

exercise_2_3_hint = (
    "The grader needs 800+ words. LLMs are poor at counting words, so overshoot your target "
    "and ask for a thorough design document."
)

exercise_3_1_hint = (
    'The grader looks for words like "incorrect", "bug", "off-by-one", or "IndexError". Give '
    "Claude a role (a meticulous senior code reviewer) that primes it to scrutinize the code."
)

exercise_4_1_hint = (
    "Keep the {FUNCTION_NAME} placeholder in your template and substitute it with str.replace. "
    "The grader checks the output mentions the function name and a test assertion (assert/def test_)."
)

exercise_4_2_hint = (
    "Wrap the noisy user ticket in XML tags (e.g. <ticket>...</ticket>) so Claude can tell your "
    'instructions apart from the user\'s messy text. The grader looks for the status code "404".'
)

exercise_4_3_hint = (
    "Remove text one piece at a time, starting with the parts that make the least sense, and watch "
    'how much Claude can still parse. The grader still looks for "404".'
)

exercise_5_1_hint = (
    "The grader looks for the XML tag <review> in the output. Ask Claude to wrap its answer in that tag."
)

exercise_5_2_hint = (
    "Ask for two clearly delimited sections. The grader checks both <summary> and <risks> tags appear."
)

exercise_5_3_hint = (
    "Use output_config.format with a json_schema so the response is guaranteed-parseable JSON. "
    'The grader parses it and checks for a "summary" string and an "issues" list.'
)

exercise_6_1_hint = (
    "Give Claude the categories explicitly, with the parenthetical letters. Let it write a short "
    "<analysis> block first, then answer (ask for an analysis, not for its 'thinking', which current "
    'models decline). The grader looks for the correct "(A)" style label.'
)

exercise_6_2_hint = (
    "Make Claude answer with ONLY the category letter: instruct it directly or use a structured "
    "output. The grader checks the final answer is exactly the category letter."
)

exercise_7_1_hint = (
    'Provide a few example "log line -> label" pairs (few-shot). The grader checks the last token '
    "of Claude's output is the correct label."
)

exercise_8_1_hint = (
    "Give Claude an out: tell it to say it doesn't know if it isn't sure. The grader checks the "
    "response admits uncertainty and does NOT invent details about the fake package."
)

exercise_8_2_hint = (
    "Tell Claude to answer ONLY from the document and to quote the relevant lines first. The grader "
    "checks Claude declines when the answer is not present in the document."
)

exercise_9_1_hint = (
    "Layer the techniques: role + tone + rules + input wrapped in XML + an explicit output format. "
    "There is no automated grader here: judge it against the success criteria and reflection questions."
)

exercise_9_2_hint = (
    "Start from the code-explainer scaffold and add: a clear role, what to do with the user's code, "
    "and a structured output. Evaluate against the success criteria, not an automated grader."
)

exercise_10_2_1_hint = (
    "Define the tool as a dict with a JSON-Schema input_schema. The loop (already written) runs while "
    'stop_reason == "tool_use", executes the tool locally, and feeds a tool_result block back. The '
    "grader checks the final answer contains the looked-up value."
)
