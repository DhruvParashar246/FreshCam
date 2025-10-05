import { View, Text, StyleSheet, ScrollView } from "react-native";
import { Ionicons } from "@expo/vector-icons";

export default function TipsScreen() {
  const tips = [
    {
      icon: "leaf-outline",
      title: "Reduce Food Waste",
      description: "Use overripe fruits in smoothies, baking, or make jams instead of throwing them away."
    },
    {
      icon: "thermometer-outline",
      title: "Proper Storage",
      description: "Store bananas at room temperature until ripe, then refrigerate to slow ripening."
    },
    {
      icon: "snow-outline",
      title: "Freeze for Later",
      description: "Freeze overripe bananas (peeled) for smoothies or banana bread later."
    },
    {
      icon: "restaurant-outline",
      title: "Meal Planning",
      description: "Plan meals based on fruit ripeness to use them at their peak freshness."
    },
    {
      icon: "planet-outline",
      title: "Environmental Impact",
      description: "Reducing food waste helps lower greenhouse gas emissions and saves water."
    },
  ];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>💡 Food Waste Tips</Text>
        <Text style={styles.subtitle}>Make the most of your fruits</Text>
      </View>

      {tips.map((tip, index) => (
        <View key={index} style={styles.tipCard}>
          <Ionicons name={tip.icon as any} size={32} color="#4CAF50" />
          <View style={styles.tipContent}>
            <Text style={styles.tipTitle}>{tip.title}</Text>
            <Text style={styles.tipDescription}>{tip.description}</Text>
          </View>
        </View>
      ))}

      <View style={styles.footer}>
        <Text style={styles.footerText}>
          FreshCam helps you make informed decisions about your food!
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f5f5",
  },
  header: {
    padding: 20,
    paddingTop: 60,
    backgroundColor: "#fff",
    marginBottom: 10,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#333",
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: "#666",
  },
  tipCard: {
    flexDirection: "row",
    backgroundColor: "#fff",
    padding: 16,
    marginHorizontal: 16,
    marginBottom: 12,
    borderRadius: 12,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  tipContent: {
    flex: 1,
    marginLeft: 16,
  },
  tipTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#333",
    marginBottom: 6,
  },
  tipDescription: {
    fontSize: 14,
    color: "#666",
    lineHeight: 20,
  },
  footer: {
    padding: 20,
    alignItems: "center",
    marginTop: 10,
    marginBottom: 40,
  },
  footerText: {
    fontSize: 14,
    color: "#999",
    textAlign: "center",
    fontStyle: "italic",
  },
});
