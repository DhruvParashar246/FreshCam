import React, { useEffect, useState } from "react";
import { View, Text, Image, TouchableOpacity, ActivityIndicator, StyleSheet } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import axios from "axios";
import { FlatColors as Colors } from "../constants/theme";

export default function ResultScreen() {
  const router = useRouter();
  const { imageUri } = useLocalSearchParams<{ imageUri: string }>(); // Get the photo from Camera
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Send to backend when the screen loads
  useEffect(() => {
    if (imageUri) {
      analyzeImage(imageUri);
    }
  }, [imageUri]);

  const analyzeImage = async (uri: string) => {
    try {
      const formData = new FormData();
      formData.append("file", {
        uri,
        type: "image/jpeg",
        name: "image.jpg",
      } as any);

      const response = await axios.post("http://192.168.1.105:8000/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(response.data);
    } catch (err) {
      setError("Failed to analyze image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={Colors.primary} />
        <Text style={{ color: Colors.text }}>Analyzing freshness...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.center}>
        <Text style={{ color: Colors.danger }}>{error}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Image source={{ uri: imageUri }} style={styles.image} />
      <Text style={styles.title}>Ripeness Result</Text>

      {result ? (
        <>
          <Text style={styles.text}>
            <Text style={{ fontWeight: "600" }}>Fruit:</Text> {result.label}
          </Text>
          <Text style={styles.text}>
            <Text style={{ fontWeight: "600" }}>Confidence:</Text> {(result.confidence * 100).toFixed(1)}%
          </Text>
          <Text style={styles.text}>
            <Text style={{ fontWeight: "600" }}>Status:</Text>{" "}
            {result.ripeness_description || "Looks fresh!"}
          </Text>
        </>
      ) : (
        <Text style={styles.text}>No data returned.</Text>
      )}

      <TouchableOpacity
        style={styles.button}
        onPress={() => router.push("/(tabs)/pantry")}
      >
        <Text style={styles.buttonText}>Add to Pantry</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    alignItems: "center",
    paddingTop: 50,
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: Colors.background,
  },
  image: {
    width: 200,
    height: 200,
    borderRadius: 10,
    marginBottom: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: Colors.text,
    marginBottom: 20,
  },
  text: {
    fontSize: 16,
    color: Colors.text,
    marginBottom: 10,
    textAlign: "center",
  },
  button: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
    marginTop: 30,
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
});
