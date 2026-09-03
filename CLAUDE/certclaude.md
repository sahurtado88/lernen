An architect is reviewing the basic structure of an agentic loop in application code. Which of the following pseudocode patterns correctly represents the Claude agentic loop?

 Call the API, check stop_reason; if "end_turn" break and return the response; if "tool_use" extract tool_use blocks, execute all tools, append assistant and tool_result messages, then loop again.

 The correct agentic loop pattern is: (1) call the API, (2) check stop_reason, (3) if "end_turn", break and return the response, (4) if "tool_use", extract tool_use blocks, execute all tools, append the assistant message and the tool_result user message to the messages list, then loop again. This mirrors the standard Claude agentic loop structure.

# agetic loops

 Agentic loop best practices: (1) max_iterations counter, (2) per-operation timeouts, (3) budget/cost limits, (4) human-in-the-loop checkpoints for sensitive actions. Never rely solely on the model to self-terminate.

# A company's agentic pipeline uses Claude with a custom stop sequence of "##DONE##". During a run, the API returns stop_reason: "stop_sequence" with the stop_sequence value set to "##DONE##". What does this indicate and what should the application do?

The agent has reached the custom completion signal; the application should exit the agentic loop and extract the content generated before the stop sequence as the final output.

# tip

"max_tokens" continuation pattern: append the truncated assistant message to messages → add user message "continue" → retry with higher max_tokens. The partial assistant content must be in the history, otherwise Claude restarts. This is called "continuation" prompting.

# A developer is building an agentic loop and notices that Claude sometimes returns a response where both text content blocks and tool_use blocks appear together in the content array. How should the application handle this mixed response?


A Store the complete assistant response (including both text and tool_use blocks) in messages history, execute all tool_use blocks, and continue the agentic loop.

# tip 

Claude decides to stop calling tools when it has enough information to answer the user's request. This is a model-level judgment, not a hard counter. Architects add max_iteration limits as external safeguards because model judgment can fail. Trust but verify with your own loop controls.

# A company is designing an agent orchestration pattern where a primary orchestrator Claude agent spawns specialized subagents for specific subtasks. The orchestrator calls a spawn_subagent tool to delegate a data retrieval task. From an architectural standpoint, what does this pattern require in the application layer?

 Implement a nested agentic loop where the spawn_subagent tool execution triggers a separate API call sequence for the subagent, runs it to completion, and returns the subagent's final output as the tool_result to the orchestrator.

# tip

Subagent spawning = nested agentic loops. Orchestrator's tool execution IS a full inner loop for the subagent. Each agent has its own messages array. The subagent's final answer becomes the tool_result for the orchestrator. Think of it as a function call that internally runs another agentic loop.

# A company's agentic pipeline encounters a scenario where Claude returns stop_reason: "tool_use", but one of the tool_use blocks references a tool name that is not defined in the tools array that was sent in the request. How should a well-architected system handle this situation?

# tip
 Always validate tool names before execution. Unknown tool → isError: true with "tool not available" message. This closes the protocol loop correctly and lets Claude adapt. Silent ignoring or crashing are both wrong. Defensive tool validation is a production agentic system best practice.

# An architect is designing a high-reliability agentic pipeline for a financial institution. The pipeline must ensure that each step of a multi-stage financial audit is auditable, recoverable, and idempotent. The agent uses tool calls to write records to a ledger system. Which combination of design principles best addresses these requirements?

Persist the messages array to durable storage after each loop iteration, implement idempotent tool calls with unique operation IDs, log every tool_use and tool_result for auditing, and enforce a max_iterations limit.

# tip

High-reliability agentic systems need: (1) durable state persistence (save messages array externally), (2) idempotent tools (unique IDs prevent duplicate writes), (3) comprehensive audit logging (every tool_use + tool_result), (4) max_iterations guard. These four pillars are the foundation of production-grade agentic pipelines.

# A company builds an agentic workflow where Claude calls a search tool repeatedly in a loop, but the developer notices that Claude never produces a stop_reason of "end_turn" — it keeps issuing search tool_use blocks indefinitely. After investigating, the developer determines that the search results are always incomplete, causing Claude to search again. What is the most architecturally sound fix?


Improve the search tool's completeness or redefine its scope in the tool description to set realistic expectations, and implement a max_iterations guard with graceful partial-result handling.

# tip

Infinite tool loops often stem from tool outputs that never satisfy the model's completion criteria. Fix: (1) improve tool data quality/scope, (2) add max_iterations guard, (3) implement graceful partial-result handling. Never rely on only one layer of protection. Root-cause fixes + application-layer guards = defense in depth.

# tip

The four stop_reason values and their actions: (1) end_turn = DONE, show user; (2) tool_use = RUN TOOLS, loop; (3) max_tokens = INCOMPLETE, handle gracefully; (4) stop_sequence = DONE (custom signal), show user. Memorize this table — it's the heart of every agentic loop.

end_turn → exit loop and present to user; 
tool_use → execute tools and continue loop; 
max_tokens → handle truncation gracefully; 
stop_sequence → exit loop.

# An architect is implementing an agentic loop in Python. Claude returns a response containing two tool_use blocks. The architect writes code to iterate over the content array and execute each tool. Before making the next API call, what must the messages array contain?

All previous messages, the assistant's response message (containing the tool_use blocks), and a new user message containing both tool_result content blocks referencing their respective tool_use_ids.

# tip

After executing N tools: messages = [...history, assistant_message_with_N_tool_uses, {role: 'user', content: [tool_result_1, tool_result_2, ..., tool_result_N]}]. One user message, N tool_result blocks. The assistant message with tool_use MUST be preserved in history.