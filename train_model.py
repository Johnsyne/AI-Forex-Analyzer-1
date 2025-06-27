import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# Load your generated training data
df = pd.read_csv("training_data_full.csv")

# Drop rows with missing values (just in case)
df.dropna(inplace=True)

# Select features used for training
features = [
    "open", "high", "low", "close", "volume",
    "rsi", "macd", "signal", "ema", "bb_upper", "bb_lower"
]
X = df[features]

# Encode target labels (BUY, SELL, NEUTRAL)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["signal_label"])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train XGBoost Classifier
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("📊 Classification Report:")
print(classification_report(
    y_test,
    y_pred,
    labels=[0, 1, 2],  # assuming the label encoder maps BUY=0, NEUTRAL=1, SELL=2
    target_names=label_encoder.classes_,
    zero_division=0
))

# Save model and encoder
joblib.dump(model, "signal_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
print("✅ Model and label encoder saved!")
