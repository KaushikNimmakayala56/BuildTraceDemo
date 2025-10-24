# 🎯 ENGINEERING DRAWING MENTOR - SIMPLE IMPLEMENTATION PLAN

---

## 📖 WHAT WE'RE BUILDING

**In One Sentence:**  
Student uploads engineering drawing problem image → AI extracts problem number → Backend retrieves ONLY that problem's section from PDF → AI generates 4-6 simple construction steps → Display clean results.

**Smart but Simple: No RAG. No vector database. No embeddings.**  
Just: Extract problem number → Find matching section → Send targeted context → Get steps.

---

## 🎯 THE FLOW

```
1. Student uploads Problem 12-12 image
2. Backend receives image
3. Backend asks Gemini: "What problem number is in this image?" → Gets "12-12"
4. Backend retrieves Problem 12-12 section from pre-parsed PDF dictionary
5. Backend sends image + ONLY that section to Gemini (500 tokens vs 7,500!)
6. Gemini returns JSON with 4-6 steps
7. Frontend displays steps in clean format
```

**Why This is Smart:**
- ✅ 60% fewer tokens (faster, more efficient)
- ✅ More focused AI responses (only sees relevant problem)
- ✅ Still super simple (just string matching, no complex ML)
- ✅ Shows optimization thinking for interview

---

## 🛠️ WHAT WE NEED TO BUILD

### **BACKEND (3 main pieces):**

1. **PDF Service (Smart Parsing)**
   - Load 12-page PDF at startup
   - Extract all text using PyPDF2
   - **Split into sections** using regex: Find "Problem 12-1", "Problem 12-2", etc.
   - Store in dictionary: `{"12-1": "section text...", "12-2": "...", "12-12": "..."}`
   - Keep in memory for fast lookup

2. **Gemini Service (Two-Step Process)**
   - **Step A:** Extract problem number from image
     - Quick Gemini call: "What problem number is shown? Return only '12-X'"
     - Parse response to get clean number
   - **Step B:** Analyze with targeted context
     - Take image + ONLY the matching problem section
     - Send to Gemini 2.0 Flash
     - Ask for JSON response with steps
     - Parse and return

3. **FastAPI Endpoints**
   - POST `/api/analyze` - Accepts image, orchestrates two-step flow, returns steps
   - GET `/api/health` - Confirms PDF loaded and shows section count
   - Handle errors gracefully (fallback to full PDF if problem number not found)

### **FRONTEND (3 main pieces):**

1. **Upload Component**
   - Drag-and-drop image upload
   - Shows image preview
   - "Analyze" button
   - Clean and simple

2. **Results Component**
   - Shows problem identified
   - Shows 4-6 numbered steps
   - Each step: instruction + explanation
   - Clean formatting

3. **Main App**
   - Coordinates upload and results
   - Shows loading spinner
   - Handles errors
   - Keep it minimal

---

## 📋 STEP-BY-STEP CHECKLIST

### **PHASE 1: BACKEND**

**Step 1: Setup**
- [ ] Install dependencies: `google-generativeai`, `PyPDF2`, `Pillow`, `python-dotenv`
- [ ] Get Gemini API key
- [ ] Place 12-page PDF in backend folder

**Step 2: PDF Service**
- [ ] Create `pdf_service.py`
- [ ] Load PDF and extract all text
- [ ] **Parse into sections** using regex (find "Problem 12-X" markers)
- [ ] Store in dictionary: `{"12-1": "text...", "12-2": "text...", ...}`
- [ ] Add fallback: `get_full_text()` if section not found
- [ ] Test: Can retrieve specific section by problem number

**Step 3: Gemini Service**
- [ ] Create `gemini_service.py`
- [ ] **Function 1:** `extract_problem_number(image)` 
  - Simple prompt: "What problem number is in this image? Return only '12-X'"
  - Parse response (e.g., "12-12")
- [ ] **Function 2:** `analyze_drawing(image, problem_section)`
  - Write prompt that includes ONLY problem section + asks for steps
  - Send image + targeted section to Gemini
  - Parse JSON response
- [ ] Test: Can extract problem number AND return structured steps

**Step 4: FastAPI Endpoints**
- [ ] Create `/api/analyze` endpoint with smart flow:
  - Accept image upload
  - **Call:** `extract_problem_number(image)` → get "12-12"
  - **Retrieve:** Problem section from PDF service
  - **Call:** `analyze_drawing(image, section)` → get steps
  - Return JSON response
- [ ] Add `/api/health` endpoint showing loaded sections
- [ ] Add error handling (fallback to full PDF if problem number fails)

**Step 5: Backend Testing**
- [ ] Test problem number extraction works
- [ ] Verify correct section retrieved (Problem 12-12 section only)
- [ ] Confirm token count reduced (~500 vs 7,500)
- [ ] Verify returns 4-6 clear steps
- [ ] Check steps reference textbook correctly
- [ ] Test fallback (image without problem number → uses full PDF)

---

### **PHASE 2: FRONTEND**

**Step 6: React Setup**
- [ ] Create clean React app structure
- [ ] Set up basic styling (CSS or Tailwind)
- [ ] Create folder structure

**Step 7: Upload Component**
- [ ] Build drag-and-drop upload
- [ ] Add image preview
- [ ] Add "Analyze" button
- [ ] Style it nicely

**Step 8: Results Component**
- [ ] Display problem title
- [ ] Show numbered steps (1, 2, 3...)
- [ ] Format instruction + explanation
- [ ] Add "Try Another" button
- [ ] Style cleanly

**Step 9: Connect to Backend**
- [ ] Create API service
- [ ] Call `/api/analyze` endpoint
- [ ] Handle loading state
- [ ] Handle errors
- [ ] Show results

**Step 10: Frontend Testing**
- [ ] Upload test image
- [ ] Verify results display
- [ ] Test all UI states
- [ ] Fix any issues

---

### **PHASE 3: POLISH & DEMO**

**Step 11: Make it Beautiful**
- [ ] Clean up UI spacing
- [ ] Add nice colors
- [ ] Make it responsive
- [ ] Add loading animations
- [ ] Polish typography

**Step 12: Final Testing**
- [ ] Test with 2-3 different problems
- [ ] Verify AI uses textbook content
- [ ] Check on different screen sizes
- [ ] Test error handling

**Step 13: Demo Prep**
- [ ] Prepare 2-3 sample images
- [ ] Write demo script
- [ ] Practice walkthrough
- [ ] Take screenshots

---

## 🎯 KEY REMINDERS

### **Keep It Simple (But Smart):**
- ✅ Parse PDF into sections at startup (one-time cost)
- ✅ Extract problem number with simple Gemini call
- ✅ Send ONLY relevant section (not entire PDF)
- ✅ Use basic string matching (no embeddings, no vector DB)
- ✅ One backend file for PDF parsing
- ✅ One backend file for Gemini calls
- ✅ Clean, minimal React components
- ✅ No over-engineering

### **Code Quality:**
- ✅ Each function does ONE thing
- ✅ Clear variable names
- ✅ Comments where needed
- ✅ Handle errors properly
- ✅ Keep files small and focused

### **Testing:**
- ✅ Test after EACH step
- ✅ Don't move forward if something broken
- ✅ Use real Problem 12-12 image
- ✅ Verify AI output is educational

### **What Success Looks Like:**
- ✅ Upload image → Extract problem number → Get 4-6 clear steps in 5-10 seconds
- ✅ AI uses ONLY the relevant problem section (efficient!)
- ✅ Steps reference correct textbook content
- ✅ Token usage optimized (500 vs 7,500)
- ✅ UI is clean and professional
- ✅ Works smoothly end-to-end
- ✅ Ready to demo with confidence
- ✅ Shows smart optimization thinking for interview

---

## 📦 DELIVERABLES

**Deliverables:**
1. Working backend API
2. Clean React frontend
3. End-to-end flow working
4. Test problems ready
5. Demo prepared

---

## 🚀 READY TO START?

**What You Need Before We Begin:**
1. ✅ Gemini API key
2. ✅ 12-page PDF file path
3. ✅ 1 test image (Problem 12-12)

**Once you have these 3 things, say "START" and we'll build step-by-step!**

---

**This is simple. This is focused. This will work.** 💪

