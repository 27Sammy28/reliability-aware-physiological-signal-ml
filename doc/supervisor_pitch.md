# Supervisor Pitch

## Short Version

My long-term research goal is to develop reliable machine learning methods for extracting actionable health information from noisy observational signals, with applications ranging from physiological monitoring to public-health surveillance systems in Africa.

## Why This Fits a Signal-Processing Health AI Lab

This project focuses on the reliability problem that appears across ECG, speech, voice, cough, and respiratory audio: real-world signals are noisy, incomplete, heterogeneous, and often shifted across devices and populations. I am interested in methods that quantify when machine-learning predictions can be trusted and when uncertainty should limit action.

## Current Testbed

The current repository uses ECG classification as a controlled physiological signal benchmark. It evaluates:

- signal corruption;
- temporal missingness;
- calibration error;
- robustness curves;
- reliability reports;
- responsible-AI limitations.

## Future Direction

The next stage is to extend this reliability framework to voice, cough, respiratory sounds, speech, and language signals for low-resource public-health surveillance. This connects naturally to Africa CDC-style needs for scalable, low-cost, and reliable disease surveillance tools.