# Manual Test Cases for Smart Sum Calculator App

---

## 1. Compute Sum – Positive Case
**Test Case ID:** TC_01  
**Input:** 10, 20, 30  
**Expected Output:**  
- Sum Result: 60  
- Transaction ID is generated  
- Timestamp is shown  
- Status: New (not cached on first request)  

---

## 2. Compute Sum – Cached Result
**Test Case ID:** TC_02  
**Input:** 10, 20, 30 (same as before)  
**Expected Output:**  
- Sum Result: 60  
- Same Transaction ID  
- Status: Cached  
- No recalculation  

---

## 3. Compute Sum – Invalid Input (Alphabets)
**Test Case ID:** TC_03  
**Input:** 10, abc, 30  
**Expected Output:**  
- Error Message: “Invalid input: 'abc' is not a number.”  

---

## 4. Compute Sum – Invalid Input (Special Characters)
**Test Case ID:** TC_04  
**Input:** 10, @, 30  
**Expected Output:**  
- Error Message: “Invalid input: '@' is not a number.”  

---

## 5. Compute Sum – Empty Input
**Test Case ID:** TC_05  
**Input:** [Leave field empty]  
**Expected Output:**  
- Error Message: “Please enter some numbers.”  

---

## 6. Compute Sum – Negative Numbers
**Test Case ID:** TC_06  
**Input:** -10, -20, 30  
**Expected Output:**  
- Sum Result: 0  
- Transaction ID and Timestamp shown  

---

## 7. Retrieve Transaction – Valid ID
**Test Case ID:** TC_07  
**Input:** Valid transaction ID (from previous tests)  
**Expected Output:**  
- Numbers used  
- Sum result  
- Timestamp  

---

## 8. Retrieve Transaction – Invalid ID
**Test Case ID:** TC_08  
**Input:** Transaction ID: 999999  
**Expected Output:**  
- Error Message: “Transaction ID not found.”  

---

## 9. UI Load Check
**Test Case ID:** TC_09  
**Action:** Open homepage `/`  
**Expected Output:**  
- Buttons for "Start Computing" and "Search by Transaction"  
- Navigation bar loads  
