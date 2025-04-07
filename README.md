# Pubdater Tool

## What is Pubdater?

Pubdater is a handy tool that helps update the dependencies in your **pubspec.yaml** file for Dart projects. It checks for the latest compatible versions of your packages based on the Dart version you're using and updates the file for you.

---

## How it Works:
1. **Extracts dependencies** from the pubspec file.
2. **Finds the latest versions** that work with your Dart SDK.
3. **Updates your pubspec file** with the new versions if they are compatible.

---

## Why Use It?
- Saves time by automating dependency updates.
- Makes sure your packages are up-to-date and compatible with your Dart version.
- Handles large, empty, or tricky pubspec files gracefully.

---

## Key Features:
- Detects all dependencies and checks their versions.
- Updates only compatible versions, keeping your project stable.
- Provides clear messages if something can't be updated.

---

## Error Handling:
If your pubspec file is too long, empty, or has no dependencies to update, Pubdater will let you know and explain the issue.

---
