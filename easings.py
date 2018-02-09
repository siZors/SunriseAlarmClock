from math import *

"""
    easeInBack: function (x, t, b, c, d, s) {
        if (s == undefined) s = 1.70158;
        return c*(t/=d)*t*((s+1)*t - s) + b;
    },
    easeOutBack: function (x, t, b, c, d, s) {
        if (s == undefined) s = 1.70158;
        return c*((t=t/d-1)*t*((s+1)*t + s) + 1) + b;
    },
    easeInOutBack: function (x, t, b, c, d, s) {
        if (s == undefined) s = 1.70158; 
        if ((t/=d/2) < 1) return c/2*(t*t*(((s*=(1.525))+1)*t - s)) + b;
        return c/2*((t-=2)*t*(((s*=(1.525))+1)*t + s) + 2) + b;
    },
    easeInBounce: function (x, t, b, c, d) {
        return c - jQuery.easing.easeOutBounce (x, d-t, 0, c, d) + b;
    },
    easeOutBounce: function (x, t, b, c, d) {
        if ((t/=d) < (1/2.75)) {
            return c*(7.5625*t*t) + b;
        } else if (t < (2/2.75)) {
            return c*(7.5625*(t-=(1.5/2.75))*t + .75) + b;
        } else if (t < (2.5/2.75)) {
            return c*(7.5625*(t-=(2.25/2.75))*t + .9375) + b;
        } else {
            return c*(7.5625*(t-=(2.625/2.75))*t + .984375) + b;
        }
    },
    easeInOutBounce: function (x, t, b, c, d) {
        if (t < d/2) return jQuery.easing.easeInBounce (x, t*2, 0, c, d) * .5 + b;
        return jQuery.easing.easeOutBounce (x, t*2-d, 0, c, d) * .5 + c*.5 + b;
    }
"""

def easeInQuad(t, b, c, d):
    t /= d
    return c * t * t + b

def easeOutQuad(t, b, c, d):
    t /= d
    return -c * t * (t - 2) + b

def easeInOutQuad(t, b, c, d):
    t /= (d / 2)
    if t < 1:
        return c / 2 * t * t + b

    t -= 1
    return -c / 2 * (t * (t - 2) - 1) + b

def easeInQuart(t, b, c, d):
    t /= d
    return c * t * t * t * t + b

def easeOutQuart(t, b, c, d):
    t = t / d - 1
    return -c * (t * t * t * t - 1) + b

def easeInOutQuart(t, b, c, d):
    t /= (d / 2)
    if t < 1:
        return c / 2 * t * t * t * t + b
    
    t -= 2
    return -c / 2 * (t * t * t * t - 2) + b

def easeInQuint(t, b, c, d):
    t /= d
    return c * t * t * t * t * t + b

def easeOutQuint(t, b, c, d):
    t = t / d - 1
    return c * (t * t * t * t * t + 1) + b

def easeInOutQuint(t, b, c, d):
    t /= (d / 2)
    if t < 1:
        return c / 2 * t * t * t * t * t + b
    t -= 2
    return c / 2 * (t * t * t * t * t + 2) + b

def easeInCubic(t, b, c, d):
    t /= d
    return c * t * t * t + b

def easeInOutCubic(t, b, c, d):
    t /= (d / 2)
    if t < 1:
        return c / 2 * t * t * t + b
    
    t -= 2
    return c / 2 * (t * t * t + 2) + b

def easeInSine(t, b, c, d):
    return -c * cos(t / d * (pi / 2)) + c + b

def easeOutSine(t, b, c, d):
    return c * sin(t / d * (pi / 2)) + b

def easeInOutSine(t, b, c, d):
    return -c / 2 * (cos(pi * t / d) - 1) + b

def easeInExpo(t, b, c, d):
    if t == 0:
        return b
    return c * pow(2, 10 * (t / d - 1)) + b

def easeOutExpo(t, b, c, d):
    if t == d:
        return b + c
    return c * (-pow(2, -10 * t / d) + 1) + b

def easeInOutExpo(t, b, c, d):
    if t == 0:
        return b
    if t == d:
        return b + c

    t /= (d / 2)
    if t < 1:
        return c / 2 * pow(2, 10 * (t - 1)) + b

    t -= 1
    return c / 2 * (-pow(2, -10 * t) + 2) + b

def easeInCirc(t, b, c, d):
    t /= d
    return -c * (sqrt(1 - t * t) - 1) + b

def easeOutCirc(t, b, c, d):
    t = t / d - 1
    return c * sqrt(1 - t * t) + b

def easeInOutCirc(t, b, c, d):
    t /= (d / 2)
    if t < 1:
        return -c / 2 * (sqrt(1 - t * t) - 1) + b

    t -= 2
    return c / 2 * (sqrt(1 - t * t) + 1) + b

def easeInElastic(t, b, c, d):
    s = 1.70158
    a = c
    
    if t == 0: return b
    t /= d
    if t == 1: return b + c

    p = d * 0.3
    if a < abs(c):
        a = c
        s = p / 4
    else:
        s = p / (2 * pi) * asin(c / a)

    t -= 1
    return -(a * pow(2, 10 * t) * sin((t * d - s) * (2 * pi) / p)) + b

def easeOutElastic(t, b, c, d):
    s, a = 1.70158, c
    
    if t == 0: return b
    t /= d
    if t == 1: return b + c

    p = d * 0.3
    if a < abs(c):
        a, s = c, p / 4
    else:
        s = p / (2 * pi) * asin(c / a)

    return a * pow(2, -10 * t) * sin((t * d - s) * (2 * pi) / p) + c + b

def easeInOutElastic(t, b, c, d):
    s, a = 1.70158, c
    
    if t == 0: return b
    t /= (d / 2)
    if t == 2: return b + c
    
    p = d * (0.3 * 1.5)
    if a < abs(c):
        a, s = c, p / 4
    else:
        s = p / (2 * pi) * asin(c / a)

    if t < 1:
        t -= 1
        return -0.5 * (a * pow(2, 10 * t) * sin((t * d - s) * (2 * pi) / p)) + b

    t -= 1
    return a * pow(2, -10 * t) * sin((t * d - s) * (2 * pi) / p ) * 0.5 + c + b
