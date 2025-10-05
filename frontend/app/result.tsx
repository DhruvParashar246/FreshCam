import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  Platform,
  ScrollView,
} from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { FlatColors as Colors } from "../constants/theme";

export default function ResultScreen() {
  const router = useRouter();
  const { imageUri } = useLocalSearchParams<{ imageUri: string }>();
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (imageUri) analyzeImage(imageUri);
  }, [imageUri]);

  const analyzeImage = async (uri: string) => {
    try {
      const formData = new FormData();
      formData.append("file", {
        uri,
        type: "image/jpeg",
        name: "image.jpg",
      } as any);

      const res = await fetch(
        "https://conciliar-dextrosinistrally-jessika.ngrok-free.dev/predict",
        {
          method: "POST",
          body: formData,
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("❌ Upload error:", err);
      setError("Failed to analyze image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={Colors.primary} />
        <Text style={styles.loadingText}>Analyzing freshness...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>{error}</Text>
      </View>
    );
  }

  return (
    <ScrollView
      contentContainerStyle={{ flexGrow: 1, justifyContent: "center" }}
      style={{ backgroundColor: "#F7FFF7" }}
    >
      <View style={styles.container}>
        <View style={styles.card}>
          <Image source={{ uri: imageUri }} style={styles.image} />
          <Text style={styles.title}>Ripeness Result</Text>

          {result && !result.error ? (
            <>
              <View style={styles.infoBox}>
                <Text style={styles.label}>Ripeness</Text>
                <Text
                  style={[
                    styles.value,
                    {
                      color:
                        result.ripeness?.toLowerCase().includes("unripe")
                          ? Colors.info
                          : result.ripeness?.toLowerCase().includes("ripe")
                          ? Colors.success
                          : Colors.danger,
                    },
                  ]}
                >
                  {result.ripeness}
                </Text>
              </View>

              <View style={styles.infoBox}>
                <Text style={styles.label}>Confidence</Text>
                <Text style={styles.value}>{result.confidence}%</Text>
              </View>
            </>
          ) : (
            <Text style={styles.text}>
              {result?.error || "No predictions returned."}
            </Text>
          )}
        </View>

        <TouchableOpacity
          style={styles.button}
          onPress={() => router.replace("/(tabs)/camera")}
          activeOpacity={0.8}
        >
          <Text style={styles.buttonText}>Take Another Photo</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    paddingVertical: 40,
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#F7FFF7",
  },
  card: {
    width: "88%",
    backgroundColor: "#fff",
    borderRadius: 30,
    alignItems: "center",
    paddingVertical: 30,
    paddingHorizontal: 20,
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 15,
    elevation: 8,
  },
  image: {
    width: 240,
    height: 240,
    borderRadius: 20,
    marginBottom: 25,
  },
  title: {
    fontSize: 26,
    fontWeight: "800",
    color: Colors.text,
    marginBottom: 25,
    textAlign: "center",
  },
  infoBox: {
    alignItems: "center",
    marginVertical: 8,
  },
  label: {
    fontSize: 15,
    fontWeight: "600",
    color: "#777",
  },
  value: {
    fontSize: 22,
    fontWeight: "700",
    marginTop: 3,
    color: Colors.primary,
  },
  text: {
    fontSize: 16,
    color: "#555",
    textAlign: "center",
    marginTop: 10,
  },
  button: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 45,
    paddingVertical: 16,
    borderRadius: 30,
    marginTop: 40,
    shadowColor: Colors.primary,
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  buttonText: {
    color: "#fff",
    fontSize: 17,
    fontWeight: "700",
  },
  loadingText: {
    color: Colors.text,
    fontSize: 16,
    marginTop: 10,
  },
  errorText: {
    color: Colors.danger,
    fontSize: 17,
    fontWeight: "600",
  },
});
