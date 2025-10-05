import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  ScrollView,
} from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { FlatColors as Colors } from "../constants/theme";

export default function ResultScreen() {
  const router = useRouter();
  const { imageUri } = useLocalSearchParams<{ imageUri: string }>();
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (imageUri) {
      analyzeImage(imageUri);
    }
  }, [imageUri]);

  const analyzeImage = async (uri: string) => {
    try {
      setLoading(true);
      setError(null);
      
      const formData = new FormData();
      formData.append("file", {
        uri,
        type: "image/jpeg",
        name: "image.jpg",
      } as any);

      const res = await fetch(
        "https://conciliar-dextrosinistrally-jessika.ngrok-free.dev/predict?include_nutrition=true",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch (err: any) {
      console.error("❌ Upload error:", err);
      setError(err.message || "Failed to analyze image. Please try again.");
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
        <Ionicons name="alert-circle" size={64} color={Colors.danger} />
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity
          style={styles.retryButton}
          onPress={() => router.back()}
        >
          <Text style={styles.buttonText}>Try Again</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Header with Back Button */}
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => router.back()}
        >
          <Ionicons name="arrow-back" size={24} color={Colors.text} />
          <Text style={styles.backText}>Back</Text>
        </TouchableOpacity>
      </View>

      {/* Image */}
      <View style={styles.imageContainer}>
        <Image source={{ uri: imageUri }} style={styles.image} />
      </View>

      {/* Results */}
      {result && !result.error ? (
        <View style={styles.resultsContainer}>
          {/* Fruit Name */}
          <Text style={styles.fruitName}>{result.fruit_name || "Unknown"}</Text>
          
          {/* Ripeness Badge */}
          <View style={[styles.badge, getRipenessColor(result.ripeness)]}>
            <Text style={styles.badgeText}>{result.ripeness || "Unknown"}</Text>
          </View>

          {/* Confidence */}
          <Text style={styles.confidence}>
            Confidence: {result.confidence}%
          </Text>

          {/* Nutrition Info */}
          {result.nutrition && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Nutrition Facts</Text>
              <View style={styles.nutritionGrid}>
                <View style={styles.nutritionItem}>
                  <Text style={styles.nutritionValue}>{result.nutrition.calories}</Text>
                  <Text style={styles.nutritionLabel}>Calories</Text>
                </View>
                <View style={styles.nutritionItem}>
                  <Text style={styles.nutritionValue}>{result.nutrition.carbs_g}g</Text>
                  <Text style={styles.nutritionLabel}>Carbs</Text>
                </View>
                <View style={styles.nutritionItem}>
                  <Text style={styles.nutritionValue}>{result.nutrition.fiber_g}g</Text>
                  <Text style={styles.nutritionLabel}>Fiber</Text>
                </View>
                <View style={styles.nutritionItem}>
                  <Text style={styles.nutritionValue}>{result.nutrition.protein_g}g</Text>
                  <Text style={styles.nutritionLabel}>Protein</Text>
                </View>
              </View>
            </View>
          )}

          {/* Environmental Impact */}
          {result.environmental_impact && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>🌍 Environmental Impact</Text>
              <Text style={styles.infoText}>
                Carbon: {result.environmental_impact.carbon_footprint_kg} kg CO₂
              </Text>
              <Text style={styles.infoText}>
                Water: {result.environmental_impact.water_usage_liters} liters
              </Text>
            </View>
          )}

          {/* Actions */}
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={() => router.back()}
          >
            <Text style={styles.buttonText}>Scan Another</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.center}>
          <Text style={styles.errorText}>
            {result?.error || "No predictions returned."}
          </Text>
        </View>
      )}
    </ScrollView>
  );
}

function getRipenessColor(ripeness: string) {
  switch (ripeness?.toLowerCase()) {
    case "ripe":
      return { backgroundColor: "#4CAF50" };
    case "unripe":
      return { backgroundColor: "#FF9800" };
    case "overripe":
      return { backgroundColor: "#F44336" };
    default:
      return { backgroundColor: "#9E9E9E" };
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    paddingTop: 50,
    paddingHorizontal: 20,
    paddingBottom: 10,
  },
  backButton: {
    flexDirection: "row",
    alignItems: "center",
  },
  backText: {
    fontSize: 16,
    color: Colors.text,
    marginLeft: 8,
    fontWeight: "500",
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: Colors.background,
    padding: 20,
  },
  loadingText: {
    color: Colors.text,
    marginTop: 15,
    fontSize: 16,
  },
  imageContainer: {
    alignItems: "center",
    marginVertical: 20,
  },
  image: {
    width: 250,
    height: 250,
    borderRadius: 15,
  },
  resultsContainer: {
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  fruitName: {
    fontSize: 32,
    fontWeight: "bold",
    color: Colors.text,
    textAlign: "center",
    textTransform: "capitalize",
    marginBottom: 10,
  },
  badge: {
    alignSelf: "center",
    paddingHorizontal: 20,
    paddingVertical: 8,
    borderRadius: 20,
    marginBottom: 10,
  },
  badgeText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
    textTransform: "uppercase",
  },
  confidence: {
    fontSize: 14,
    color: "#666",
    textAlign: "center",
    marginBottom: 30,
  },
  section: {
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: Colors.text,
    marginBottom: 12,
  },
  nutritionGrid: {
    flexDirection: "row",
    justifyContent: "space-around",
  },
  nutritionItem: {
    alignItems: "center",
  },
  nutritionValue: {
    fontSize: 20,
    fontWeight: "bold",
    color: Colors.primary,
  },
  nutritionLabel: {
    fontSize: 12,
    color: "#666",
    marginTop: 4,
  },
  infoText: {
    fontSize: 14,
    color: Colors.text,
    marginBottom: 8,
  },
  errorText: {
    color: Colors.danger,
    fontSize: 16,
    textAlign: "center",
    marginTop: 10,
  },
  primaryButton: {
    backgroundColor: Colors.primary,
    paddingVertical: 16,
    borderRadius: 12,
    marginTop: 20,
    alignItems: "center",
  },
  retryButton: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
    marginTop: 20,
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
});
