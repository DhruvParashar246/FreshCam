import React from "react";
import { Tabs } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { Colors } from "../../constants/theme";

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: Colors.primary,
        tabBarInactiveTintColor: "#999",
        tabBarLabelStyle: { fontSize: 12, paddingBottom: 5 },
      }}
    >
      <Tabs.Screen
        name="camera"
        options={{
          title: "FreshCam",
          tabBarIcon: ({ color }) => (
            <Ionicons name="camera-outline" size={24} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="tips"
        options={{
          title: "Tips",
          tabBarIcon: ({ color }) => (
            <Ionicons name="bulb-outline" size={24} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
