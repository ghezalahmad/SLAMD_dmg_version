import numpy as np
import pandas as pd
import os

from lolopy.learners import RandomForestRegressor

# 🧠 Force PyInstaller to detect jpype even if it's indirectly used
import jpype
from jpype import startJVM, isJVMStarted

LOLO_JAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'jars', 'lolo-0.7.3.jar'))

if not isJVMStarted():
    print(f"🧪 Starting JVM with: {LOLO_JAR}")
    startJVM(classpath=[LOLO_JAR])

LOLOPY_MINIMUM_DATA_POINTS = 8

class SlamdRandomForest(RandomForestRegressor):
    def fit(self, X, y, weights=None, random_seed=42):
        if y.shape[0] < LOLOPY_MINIMUM_DATA_POINTS:
            X = np.tile(X, (4, 1))
            y = np.tile(y, (4, 1))
        y = pd.DataFrame(y)
        return super().fit(X, y, weights, random_seed)
