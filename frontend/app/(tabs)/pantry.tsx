import { View, Text, StyleSheet } from "react-native";

export default function PantryScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>PantryScreen</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#fff",
  },
  text: {
    fontSize: 22,
    fontWeight: "600",
  },
});
