import { View, Text, StyleSheet } from "react-native";

export default function TipsScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>TipsScreen</Text>
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
