The algorithm paper (.pdf file) is slightly outdated. These are the modifications:
1. Change the norm from L4 to L5;
2. Change the Stream Booster such that it boosts actual streams rather than chordstreams;
3. Add a JackNerfer;
4. Use local key-count (which calculates the number of non-empty columns in the window) in certain calculations;
5. Ignore locally empty columns for Unevenness.

Updates on Feb 2-3, 2025:
1. Increase StreamBooster to 1.7e-7;
2. Change (lambda_2, lambda_4) to (6, 0.8);
3. Incorporate difficulty at percentile points in final SR calculation;
4. Improve the dks computation to avoid unwanted suppression of Abar;
5. As a result of 4, adjust the final SR formula to maintain scaling.

Steps to use this program:
1. Create a Test folder next to the python files;
2. Throw .osu files in the Test folder;
3. Run test.py.
