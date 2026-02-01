# 🎯 Vibe Coding Tips & Best Practices

## What is Vibe Coding?

**Vibe Coding** = Conversational programming where you describe what you want and AI generates the code.

**Traditional Coding**:
```
Learn syntax → Memorize APIs → Write code → Debug errors → Repeat
```

**Vibe Coding**:
```
Describe goal → AI generates → Review → Test → Iterate
```

---

## ✅ How to Write Effective Prompts

### 1. Be Specific About What You Want

❌ **Bad**: "Make a function"

✅ **Good**: "Create a TypeScript function that takes current glucose (number) and previous glucose (number), calculates the rate of change, and returns 'rising', 'falling', or 'stable'"

### 2. Include Context

❌ **Bad**: "Add a button"

✅ **Good**: "Add a large, high-contrast button to the GlucoseStatusScreen that reads the current message aloud using text-to-speech. The button should be at least 44x44pt for senior accessibility."

### 3. Specify Input/Output Format

❌ **Bad**: "Process glucose data"

✅ **Good**: 
```
"Create a function that:
- Input: Array of {timestamp: string, glucose: number}
- Output: {state: string, message: string, trend: string}
- Logic: Classify based on latest reading and trend"
```

### 4. Mention Constraints

✅ **Good**: "Create this function WITHOUT using external libraries, just vanilla TypeScript"

✅ **Good**: "Keep the message under 2 sentences and use plain language suitable for seniors"

---

## 🎨 Prompt Templates

### For Creating New Files

```
"Help me create a TypeScript file at [path] that [purpose].

Structure:
- [Component/function 1]
- [Component/function 2]

Requirements:
- [Requirement 1]
- [Requirement 2]

Include TypeScript types and comments explaining the logic."
```

### For Debugging

```
"I'm getting this error: [paste error]

Here's my code: [paste code]

What's wrong and how do I fix it?"
```

### For Refactoring

```
"Review this code and suggest improvements for:
- Readability
- Performance
- Accessibility (for seniors)

[paste code]"
```

### For Learning

```
"Explain [concept] like I'm new to programming.

Then show me a simple example in TypeScript."
```

---

## 💡 Pro Tips

### 1. Start Simple, Then Iterate

**First prompt**: "Create a basic glucose state classifier"

**Second prompt**: "Now add time-of-day context"

**Third prompt**: "Add error handling for invalid inputs"

### 2. Ask for Explanations

After getting code:
> "Explain what this function does line by line"

### 3. Request Tests

> "Create test cases for this function with 5 different scenarios"

### 4. Get Multiple Options

> "Show me 3 different ways to implement this, with pros/cons of each"

### 5. Ask for Best Practices

> "Is this the best way to do this in TypeScript? What would a senior developer do?"

---

## 🚫 Common Mistakes to Avoid

### 1. Being Too Vague

❌ "Make it work"  
✅ "The function should return 'Stable' when glucose is between 70-140 mg/dL"

### 2. Not Providing Context

❌ "Fix this error"  
✅ "I'm getting a TypeScript error in glucoseStates.ts line 15. Here's the error: [paste]. Here's the surrounding code: [paste]"

### 3. Asking for Everything at Once

❌ "Build the entire app"  
✅ "Create the state classification function first, then we'll add the UI"

### 4. Not Testing Generated Code

Always:
1. Review the code
2. Run it
3. Test edge cases
4. Ask follow-up questions if unclear

### 5. Not Documenting What You Learn

After solving a problem:
- Note what worked
- Save the prompt that helped
- Document for future reference

---

## 🔄 The Iteration Cycle

```
1. Ask Antigravity
   ↓
2. Review generated code
   ↓
3. Test it
   ↓
4. Does it work?
   ├─ Yes → Document & move on
   └─ No → Refine prompt & repeat
```

---

## 📝 Example: Building a Feature Start-to-Finish

### Goal: Create a glucose trend calculator

#### Round 1: Basic Structure
**Prompt**:
> "Create a TypeScript function called calculateTrend that takes two numbers (current glucose and previous glucose) and returns 'rising', 'falling', or 'stable'"

**Result**: Basic function created ✓

---

#### Round 2: Add Logic
**Prompt**:
> "Update calculateTrend to consider the rate of change. If glucose changes by more than 5 mg/dL per 5 minutes, it's rising/falling. Otherwise, stable."

**Result**: Logic added ✓

---

#### Round 3: Add Types
**Prompt**:
> "Create a TypeScript type for the return value and add proper type annotations"

**Result**: Types added ✓

---

#### Round 4: Add Error Handling
**Prompt**:
> "Add error handling for invalid inputs (negative numbers, NaN, etc.)"

**Result**: Robust function ✓

---

#### Round 5: Add Tests
**Prompt**:
> "Create 5 test cases covering normal, edge, and error scenarios"

**Result**: Tests created ✓

---

## 🎯 Prompts for Common Tasks

### Creating a TypeScript Function
```
"Create a TypeScript function that:
- Name: [functionName]
- Inputs: [param1: type, param2: type]
- Output: [returnType]
- Logic: [description]
- Include error handling and comments"
```

### Creating a React Component
```
"Create a React Native component called [ComponentName] that:
- Displays: [what it shows]
- Props: [list props]
- Styling: [high contrast, large fonts for seniors]
- Accessibility: [VoiceOver compatible]"
```

### Debugging
```
"I'm getting this error:
[paste full error]

In this file:
[file path]

Here's the relevant code:
[paste code]

What's the issue and how do I fix it?"
```

### Refactoring
```
"Refactor this code to be:
- More readable
- More efficient
- Better typed (TypeScript)

[paste code]

Explain what you changed and why."
```

---

## 🌟 Advanced Techniques

### 1. Chain of Thought Prompting
```
"Let's build a message template system step by step:

Step 1: Define the data structure for messages
Step 2: Create a function to select the right message
Step 3: Add personalization logic
Step 4: Test with examples

Start with Step 1."
```

### 2. Ask for Alternatives
```
"Show me 3 ways to implement this feature:
1. Simplest (easiest to understand)
2. Most performant
3. Most maintainable

Explain trade-offs of each."
```

### 3. Request Code Reviews
```
"Review this code as if you were a senior developer:
- What's good?
- What could be improved?
- Any potential bugs?
- Accessibility concerns?

[paste code]"
```

---

## 📚 Learning Resources

### When to Ask Antigravity
- ✅ How to implement something
- ✅ Why code isn't working
- ✅ Best practices
- ✅ Explanations of concepts
- ✅ Code reviews

### When to Read Docs
- 📖 API references (Expo, React Native)
- 📖 Framework-specific patterns
- 📖 Official examples

### When to Ask Kehlin
- 👤 Glucose domain questions
- 👤 Product decisions
- 👤 User experience choices
- 👤 Clinical accuracy

---

## 🎓 Remember

1. **Antigravity is your pair programmer** - Use it constantly!
2. **Iterate, don't perfect** - First version doesn't need to be flawless
3. **Ask "why"** - Don't just copy code, understand it
4. **Document learnings** - Future you will thank you
5. **Celebrate progress** - Every working function is a win! 🎉

---

**Pro Tip**: Save your best prompts! When you find a prompt that works really well, copy it to your notes for future use.

---

**Last Updated**: January 31, 2026
