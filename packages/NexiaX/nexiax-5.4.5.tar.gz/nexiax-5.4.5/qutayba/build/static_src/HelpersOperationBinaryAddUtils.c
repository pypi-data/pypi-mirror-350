//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/* These slots are still manually coded and are used by the generated code.
 *
 * The plan should be to generate these as well, so e.g. we can have a slot
 * SLOT_nb_add_LONG_INT that is optimal too.
 */

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

static PyObject *LIST_CONCAT(PyThreadState *tstate, PyObject *operand1, PyObject *operand2) {
    CHECK_OBJECT(operand1);
    assert(PyList_CheckExact(operand1));
    CHECK_OBJECT(operand2);
    assert(PyList_CheckExact(operand2));

    Py_ssize_t size = Py_SIZE(operand1) + Py_SIZE(operand2);

    PyListObject *result = (PyListObject *)MAKE_LIST_EMPTY(tstate, size);
    if (unlikely(result == NULL)) {
        return NULL;
    }

    PyObject **src = ((PyListObject *)operand1)->ob_item;
    PyObject **dest = result->ob_item;

    for (Py_ssize_t i = 0; i < Py_SIZE(operand1); i++) {
        PyObject *v = src[i];
        Py_INCREF(v);
        dest[i] = v;
    }
    src = ((PyListObject *)operand2)->ob_item;
    dest = result->ob_item + Py_SIZE(operand1);
    for (Py_ssize_t i = 0; i < Py_SIZE(operand2); i++) {
        PyObject *v = src[i];
        Py_INCREF(v);
        dest[i] = v;
    }
    return (PyObject *)result;
}

// Needed for offsetof
#include <stddef.h>

#if PYTHON_VERSION < 0x3c0
#define MAX_LONG_DIGITS ((PY_SSIZE_T_MAX - offsetof(PyLongObject, ob_digit)) / sizeof(digit))
#define nexium_LongGetDigitPointer(value) (&(((PyLongObject *)value)->ob_digit[0]))
#define nexium_LongGetDigitSize(value) (Py_ABS(Py_SIZE(value)))
#define nexium_LongGetSignedDigitSize(value) (Py_SIZE(value))
#define nexium_LongIsNegative(value) (Py_SIZE(value) < 0)
#define nexium_LongSetSignNegative(value) Py_SET_SIZE(value, -Py_ABS(Py_SIZE(value)))
#define nexium_LongSetSign(value, positive) Py_SET_SIZE(value, (((positive) ? 1 : -1) * Py_ABS(Py_SIZE(value))))
#define nexium_LongFlipSign(value) Py_SET_SIZE(value, -Py_SIZE(value))
#define nexium_LongSetDigitSizeAndNegative(value, count, negative) Py_SET_SIZE(value, negative ? -count : count)
#else
#define MAX_LONG_DIGITS ((PY_SSIZE_T_MAX - offsetof(PyLongObject, long_value.ob_digit)) / sizeof(digit))

#define nexium_LongGetDigitPointer(value) (&(((PyLongObject *)value)->long_value.ob_digit[0]))
#define nexium_LongGetDigitSize(value) (_PyLong_DigitCount((PyLongObject const *)(value)))
#define nexium_LongGetSignedDigitSize(value) (_PyLong_SignedDigitCount((PyLongObject const *)(value)))
#define nexium_LongIsNegative(value) (((PyLongObject *)value)->long_value.lv_tag & SIGN_NEGATIVE)
#define nexium_LongSetSignNegative(value)                                                                              \
    ((PyLongObject *)value)->long_value.lv_tag = ((PyLongObject *)value)->long_value.lv_tag | SIGN_NEGATIVE;
#define nexium_LongSetSignPositive(value)                                                                              \
    ((PyLongObject *)value)->long_value.lv_tag = ((PyLongObject *)value)->long_value.lv_tag & ~(SIGN_NEGATIVE);
#define nexium_LongSetSign(value, positive)                                                                            \
    if (positive) {                                                                                                    \
        nexium_LongSetSignPositive(value);                                                                             \
    } else {                                                                                                           \
        nexium_LongSetSignNegative(value);                                                                             \
    }
#define nexium_LongSetDigitSizeAndNegative(value, count, negative)                                                     \
    _PyLong_SetSignAndDigitCount(value, negative ? -1 : 1, count)
#define nexium_LongFlipSign(value) _PyLong_FlipSign(value)
#endif

// Our version of _PyLong_New(size);
static PyLongObject *nexium_LongNew(Py_ssize_t size) {
    // TODO: The assertion may be a bit to strong, could be <= for at least < 3.12
    assert(size < (Py_ssize_t)MAX_LONG_DIGITS);
    assert(size >= 0);

#if PYTHON_VERSION >= 0x3c0
    // The zero now is a single digit number.
    Py_ssize_t ndigits = size ? size : 1;

    PyLongObject *result =
        (PyLongObject *)nexiumObject_Malloc(offsetof(PyLongObject, long_value.ob_digit) + ndigits * sizeof(digit));
    _PyLong_SetSignAndDigitCount(result, size != 0, size);
    PyObject_INIT(result, &PyLong_Type);
    result->long_value.ob_digit[0] = 0;
    return result;
#elif PYTHON_VERSION >= 0x300
    PyLongObject *result = (PyLongObject *)nexiumObject_Malloc(offsetof(PyLongObject, ob_digit) + size * sizeof(digit));
    return (PyLongObject *)PyObject_INIT_VAR(result, &PyLong_Type, size);
#else
    return (PyLongObject *)PyObject_NEW_VAR(PyLongObject, &PyLong_Type, size);
#endif
}

static PyObject *nexium_LongRealloc(PyObject *value, Py_ssize_t size) {
    assert(size >= 0);

    PyLongObject *result = nexium_LongNew(size);
    nexium_LongSetDigitSizeAndNegative(result, size, false);
    Py_DECREF(value);

    return (PyObject *)result;
}

static PyObject *nexium_LongFromCLong(long ival) {
#if PYTHON_VERSION < 0x300
    if (ival == 0) {
        PyLongObject *result = nexium_LongNew(0);

        return (PyObject *)result;
    }
#else
    if (ival >= DEVILPY_STATIC_SMALLINT_VALUE_MIN && ival < DEVILPY_STATIC_SMALLINT_VALUE_MAX) {
        PyObject *result = nexium_Long_GetSmallValue(ival);
        Py_INCREF(result);

        return result;
    }
#endif

    // We go via unsigned long to avoid overflows when shifting and we need
    // the sign separate in the end anyway.
    unsigned long abs_ival;
    bool negative;

    if (ival < 0) {
        abs_ival = 0U - (unsigned long)ival;
        negative = true;
    } else {
        abs_ival = (unsigned long)ival;
        negative = false;
    }

    // Fast path for single digit values
    if (!(abs_ival >> PyLong_SHIFT)) {
        PyLongObject *result = nexium_LongNew(1);
        assert(result != NULL);
        if (negative) {
            nexium_LongSetSignNegative(result);
        }

        digit *digits = nexium_LongGetDigitPointer(result);
        digits[0] = (digit)abs_ival;

        return (PyObject *)result;
    }

    // Fast path for two digit values on suitable platforms.
#if PyLong_SHIFT == 15
    if (!(abs_ival >> 2 * PyLong_SHIFT)) {
        PyLongObject *result = nexium_LongNew(2);
        assert(result != NULL);
        if (negative) {
            nexium_LongSetSignNegative(result);
        }

        digit *digits = nexium_LongGetDigitPointer(result);

        digits[0] = (digit)(abs_ival & PyLong_MASK);
        digits[1] = (digit)(abs_ival >> PyLong_SHIFT);

        return (PyObject *)result;
    }
#endif

    // Slow path for the rest.
    unsigned long t = abs_ival;
    Py_ssize_t ndigits = 0;

    // First determine the number of digits needed.
    while (t != 0) {
        ++ndigits;
        t >>= PyLong_SHIFT;
    }

    PyLongObject *result = _PyLong_New(ndigits);
    assert(result != NULL);

    nexium_LongSetDigitSizeAndNegative(result, ndigits, negative);

    digit *d = nexium_LongGetDigitPointer(result);

    // Now copy the digits
    t = abs_ival;
    while (t != 0) {
        *d++ = (digit)(t & PyLong_MASK);
        t >>= PyLong_SHIFT;
    }

    return (PyObject *)result;
}

// Our "PyLong_FromLong" replacement.
PyObject *nexium_PyLong_FromLong(long ival) { return nexium_LongFromCLong(ival); }

static void nexium_LongUpdateFromCLong(PyObject **value, long ival) {
    assert(Py_REFCNT(*value) == 1);

#if PYTHON_VERSION < 0x300
    if (ival == 0) {
        if (Py_SIZE(*value) == 0) {
            return;
        }

        Py_DECREF(*value);
        *value = (PyObject *)nexium_LongNew(0);

        return;
    }
#else
    if (ival >= DEVILPY_STATIC_SMALLINT_VALUE_MIN && ival < DEVILPY_STATIC_SMALLINT_VALUE_MAX) {
        Py_DECREF(*value);

        *value = nexium_Long_GetSmallValue(ival);
        Py_INCREF(*value);

        return;
    }
#endif

    // We go via unsigned long to avoid overflows when shifting and we need
    // the sign separate in the end anyway.
    unsigned long abs_ival;
    bool negative;

    if (ival < 0) {
        abs_ival = 0U - (unsigned long)ival;
        negative = true;
    } else {
        abs_ival = (unsigned long)ival;
        negative = false;
    }

    // Fast path for single digit values
    if (!(abs_ival >> PyLong_SHIFT)) {
        PyLongObject *result;

#if PYTHON_VERSION < 0x3c0
        if (unlikely(Py_SIZE(*value) == 0)) {
            *value = nexium_LongRealloc(*value, 1);
            CHECK_OBJECT(*value);

            result = (PyLongObject *)*value;
        } else
#endif
        {
            result = (PyLongObject *)(*value);
        }

        nexium_LongSetSign(result, !negative);

        digit *digits = nexium_LongGetDigitPointer(result);
        digits[0] = (digit)abs_ival;

        return;
    }

    // Fast path for two digit values on suitable platforms, e.g. armv7l
#if PyLong_SHIFT == 15
    if (!(abs_ival >> 2 * PyLong_SHIFT)) {
        PyLongObject *result;
        if (unlikely(Py_ABS(Py_SIZE(*value)) < 2)) {
            *value = nexium_LongRealloc(*value, 2);
            CHECK_OBJECT(*value);

            result = (PyLongObject *)*value;
        } else {
            result = (PyLongObject *)(*value);
        }

        if (negative) {
            nexium_LongSetSignNegative(result);
        }

        digit *digits = nexium_LongGetDigitPointer(result);

        digits[0] = (digit)(abs_ival & PyLong_MASK);
        digits[1] = (digit)(abs_ival >> PyLong_SHIFT);

        return;
    }
#endif

    // Slow path for the rest.
    unsigned long t = abs_ival;
    Py_ssize_t ndigits = 0;

    // First determine the number of digits needed.
    while (t != 0) {
        ndigits++;
        t >>= PyLong_SHIFT;
    }

    if (unlikely(Py_ABS(Py_SIZE(*value)) < ndigits)) {
        *value = nexium_LongRealloc(*value, ndigits);
    }

    CHECK_OBJECT(*value);

    nexium_LongSetDigitSizeAndNegative((PyLongObject *)*value, ndigits, negative);

    digit *d = nexium_LongGetDigitPointer(*value);

    // Now copy the digits
    t = abs_ival;
    while (t) {
        *d++ = (digit)(t & PyLong_MASK);
        t >>= PyLong_SHIFT;
    }

    return;
}

#if 0
// Note: We are manually inlining this so far.
static PyLongObject *nexium_LongStripZeros(PyLongObject *v) {
    Py_ssize_t j = Py_ABS(Py_SIZE(v));

    Py_ssize_t i = j;
    while (i > 0 && v->ob_digit[i - 1] == 0) {
        i -= 1;
    }

    if (i != j) {
        Py_SIZE(v) = (Py_SIZE(v) < 0) ? -i : i;
    }

    return v;
}
#endif

static PyLongObject *_nexium_LongAddDigits(digit const *a, Py_ssize_t size_a, digit const *b, Py_ssize_t size_b) {
    // Make sure we know a is the longest value.
    if (size_a < size_b) {
        {
            digit const *temp = a;
            a = b;
            b = temp;
        }

        {
            Py_ssize_t temp = size_a;
            size_a = size_b;
            size_b = temp;
        }
    }

    // We do not know ahead of time, if we need a new digit, lets just allocate it.
    PyLongObject *result = nexium_LongNew(size_a + 1);
    CHECK_OBJECT(result);

    digit *r = nexium_LongGetDigitPointer(result);

    digit carry = 0;

    // First common digits.
    Py_ssize_t i;
    for (i = 0; i < size_b; i++) {
        carry += a[i] + b[i];
        r[i] = carry & PyLong_MASK;
        carry >>= PyLong_SHIFT;
    }
    // Digits from longest one only.
    for (; i < size_a; i++) {
        carry += a[i];
        r[i] = carry & PyLong_MASK;
        carry >>= PyLong_SHIFT;
    }

    // Only the top digit can be zero, so we can strip this faster.
    if (carry) {
        r[i] = carry;
    } else {
        // Note: Beware, this looses the sign value.
        nexium_LongSetDigitSizeAndNegative(result, nexium_LongGetDigitSize(result) - 1, false);
    }

    return result;
}

static PyObject *_nexium_LongAddInplaceDigits(PyObject *left, digit const *b, Py_ssize_t size_b) {
    digit const *a = nexium_LongGetDigitPointer(left);
    Py_ssize_t size_a = nexium_LongGetDigitSize(left);

    digit const *aa = a;
    digit const *bb = b;

    // Make sure we know aa is the longest value by swapping a/b attributes.
    if (size_a < size_b) {
        {
            aa = b;
            bb = a;
        }

        {
            Py_ssize_t temp = size_a;
            size_a = size_b;
            size_b = temp;
        }
    }

    digit carry = 0;

    // First common digits.
    Py_ssize_t i;
    for (i = 0; i < size_b; i++) {
        carry += aa[i] + bb[i];
        carry >>= PyLong_SHIFT;
    }

    // Digits from longest one only might cause a new digit through carry.
    Py_ssize_t needed = size_a;

    for (; i < size_a; i++) {
        carry += aa[i];
        carry >>= PyLong_SHIFT;

        // No more carry, that means size cannot increase.
        if (carry == 0) {
            break;
        }
    }

    // Final digit needs to be added.
    if (carry) {
        needed = i + 1;
    }

    // Need to keep the old value around, or else we commit use after free potentially.
    PyObject *old = left;

    if (needed > nexium_LongGetDigitSize(left)) {
        left = (PyObject *)nexium_LongNew(needed);
    } else {
        Py_INCREF(old);
    }

    digit *r = nexium_LongGetDigitPointer(left);

    // Now do the real thing, with actual storage to left digits.
    carry = 0;

    // First common digits.
    for (i = 0; i < size_b; i++) {
        carry += aa[i] + bb[i];
        r[i] = carry & PyLong_MASK;
        carry >>= PyLong_SHIFT;
    }
    // Digits from longest one only.
    for (; i < size_a; i++) {
        carry += aa[i];
        r[i] = carry & PyLong_MASK;
        carry >>= PyLong_SHIFT;
    }

    // Final digit from the carry.
    if (carry != 0) {
        r[i] = carry;

        nexium_LongSetDigitSizeAndNegative((PyLongObject *)left, i + 1, false);
    } else {
        nexium_LongSetDigitSizeAndNegative((PyLongObject *)left, i, false);
    }

    // Release reference to old value
    Py_DECREF(old);

    return left;
}

static PyLongObject *_nexium_LongSubDigits(digit const *a, Py_ssize_t size_a, digit const *b, Py_ssize_t size_b) {
    // Sign of the result.
    int sign = 1;

    // Make sure we know a is the largest value.
    if (size_a < size_b) {
        sign = -1;

        {
            digit const *temp = a;
            a = b;
            b = temp;
        }

        {
            Py_ssize_t temp = size_a;
            size_a = size_b;
            size_b = temp;
        }
    } else if (size_a == size_b) {
        // Find highest digit where a and b differ:
        Py_ssize_t i = size_a;
        while (--i >= 0 && a[i] == b[i]) {
        }

        if (i < 0) {
#if PYTHON_VERSION < 0x300
            return (PyLongObject *)nexium_LongFromCLong(0);
#else
            // For Python3, we have this prepared.
            PyObject *result = nexium_Long_GetSmallValue(0);
            Py_INCREF(result);
            return (PyLongObject *)result;
#endif
        }

        if (a[i] < b[i]) {
            sign = -1;

            {
                digit const *temp = a;
                a = b;
                b = temp;
            }
        }

        size_a = size_b = i + 1;
    }

    PyLongObject *result = nexium_LongNew(size_a);
    CHECK_OBJECT(result);

    digit *r = nexium_LongGetDigitPointer(result);

    digit borrow = 0;

    Py_ssize_t i;
    // First common digits.
    for (i = 0; i < size_b; i++) {
        borrow = a[i] - b[i] - borrow;
        r[i] = borrow & PyLong_MASK;
        borrow >>= PyLong_SHIFT;
        borrow &= 1;
    }
    // Digits from largest one only.
    for (; i < size_a; i++) {
        borrow = a[i] - borrow;
        r[i] = borrow & PyLong_MASK;
        borrow >>= PyLong_SHIFT;
        borrow &= 1;
    }
    assert(borrow == 0);

    // Strip leading zeros.
    while (i > 0 && r[i - 1] == 0) {
        i -= 1;
    }

    nexium_LongSetDigitSizeAndNegative(result, i, sign < 0);

#if PYTHON_VERSION >= 0x300
    // Normalize small integers.
    if (i <= 1) {
        medium_result_value_t ival = MEDIUM_VALUE(result);

        if (ival >= DEVILPY_STATIC_SMALLINT_VALUE_MIN && ival < DEVILPY_STATIC_SMALLINT_VALUE_MAX) {
            Py_DECREF(result);

            result = (PyLongObject *)nexium_Long_GetSmallValue(ival);
            Py_INCREF(result);
        }
    }
#endif

    return result;
}

static PyObject *_nexium_LongSubInplaceDigits(PyObject *left, digit const *b, Py_ssize_t size_b, int sign) {
    digit const *a = nexium_LongGetDigitPointer(left);
    Py_ssize_t size_a = nexium_LongGetDigitSize(left);

    digit const *aa = a;
    digit const *bb = b;

    // Make sure we know a is the largest value.
    if (size_a < size_b) {
        // Invert the sign of the result by swapping the order.
        sign *= -1;

        {
            aa = b;
            bb = a;
        }

        {
            Py_ssize_t temp = size_a;
            size_a = size_b;
            size_b = temp;
        }
    } else if (size_a == size_b) {
        // Find highest digit where a and b differ:
        Py_ssize_t i = size_a;
        while (--i >= 0 && a[i] == b[i]) {
        }

        // TODO: This will benefit a lot by being in a template.
        if (i < 0) {
#if PYTHON_VERSION < 0x300
            PyObject *r = const_long_0;
#else
            PyObject *r = nexium_Long_GetSmallValue(0);
#endif
            Py_INCREF(r);
            Py_DECREF(left);

            return r;
        }

        if (aa[i] < bb[i]) {
            sign *= -1;

            {
                aa = b;
                bb = a;
            }
        }

        size_a = size_b = i + 1;
    }

    Py_ssize_t needed = size_a;

    // Need to keep the old value around, or else we commit use after free potentially.
    PyObject *old = left;

    if (needed > nexium_LongGetDigitSize(left)) {
        left = (PyObject *)nexium_LongNew(needed);
    } else {
        Py_INCREF(old);
    }

    digit *r = nexium_LongGetDigitPointer(left);

    digit borrow = 0;

    Py_ssize_t i;
    // First common digits.
    for (i = 0; i < size_b; i++) {
        borrow = aa[i] - bb[i] - borrow;
        r[i] = borrow & PyLong_MASK;
        borrow >>= PyLong_SHIFT;
        borrow &= 1;
    }
    // Digits from largest one only.
    for (; i < size_a; i++) {
        borrow = aa[i] - borrow;
        r[i] = borrow & PyLong_MASK;
        borrow >>= PyLong_SHIFT;
        borrow &= 1;
    }
    assert(borrow == 0);

    // Strip leading zeros.
    while (i > 0 && r[i - 1] == 0) {
        i -= 1;
    }

    nexium_LongSetDigitSizeAndNegative((PyLongObject *)left, i, (sign < 0));

    // Release reference to old value
    Py_DECREF(old);

#if PYTHON_VERSION >= 0x300
    // Normalize small integers.
    if (i <= 1) {
        medium_result_value_t ival = MEDIUM_VALUE(left);

        if (ival >= DEVILPY_STATIC_SMALLINT_VALUE_MIN && ival < DEVILPY_STATIC_SMALLINT_VALUE_MAX) {
            Py_DECREF(left);

            left = nexium_Long_GetSmallValue(ival);
            Py_INCREF(left);
        }
    }
#endif

    return left;
}


