import React, { useState } from "react";
import { View, Text, StyleSheet, FlatList, TouchableOpacity } from "react-native";

// Example scanned items
const scannedItems = [
  { id: "1", name: "Banana" },
  { id: "2", name: "Apple" },
  { id: "3", name: "Orange" },
];

export default function PantryScreen() {
  const [pantry, setPantry] = useState<string[]>([]);

  const addToPantry = (itemName: string) => {
    if (!pantry.includes(itemName)) {
      setPantry((prev) => [...prev, itemName]);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.heading}>Scanned Items</Text>
      <FlatList
        data={scannedItems}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.itemRow}>
            <Text style={styles.itemText}>{item.name}</Text>
            <TouchableOpacity
              style={styles.addButton}
              onPress={() => addToPantry(item.name)}
            >
              <Text style={styles.addButtonText}>Add to Pantry</Text>
            </TouchableOpacity>
          </View>
        )}
      />

      <Text style={styles.heading}>Your Pantry</Text>
      {pantry.length === 0 ? (
        <Text style={styles.emptyText}>No items in pantry</Text>
      ) : (
        <FlatList
          data={pantry}
          keyExtractor={(item) => item}
          renderItem={({ item }) => (
            <View style={styles.pantryItem}>
              <Text style={styles.itemText}>{item}</Text>
            </View>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: "#f7f7f7",
  },
  heading: {
    fontSize: 22,
    fontWeight: "700",
    marginVertical: 12,
    color: "#333",
  },
  itemRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#fff",
    padding: 12,
    borderRadius: 10,
    marginBottom: 8,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  itemText: {
    fontSize: 18,
    color: "#111",
  },
  addButton: {
    backgroundColor: "#4ecdc4",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  addButtonText: {
    color: "#fff",
    fontWeight: "600",
  },
  pantryItem: {
    backgroundColor: "#e0f7f5",
    padding: 10,
    borderRadius: 8,
    marginBottom: 6,
  },
  emptyText: {
    fontSize: 16,
    color: "#888",
    fontStyle: "italic",
  },
});
