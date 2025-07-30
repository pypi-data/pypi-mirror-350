# vcs - A Lightweight Git-like Version Control System

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, educational version control system implemented in Python that demonstrates the core concepts behind Git. Perfect for learning how version control systems work internally.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Commands](#-commands)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

`vcs` is a minimal version control system that implements the fundamental concepts of Git in a simplified manner. It provides content tracking through blob and tree objects, commit history with parent-child relationships, staging area for preparing commits, and basic authentication for access control.

---

## 🧰 Features

- **Repository initialization** (`vcs init`)
- **User authentication** (`vcs auth`)
- **File staging** (`vcs add`)
- **Commit creation** (`vcs commit`)
- **History viewing** (`vcs log`)
- **Commit inspection** (`vcs show`)
- **Version checkout** (`vcs checkout`)
- **Compressed storage** using zlib for efficient space usage
- **Content-based addressing** with SHA-1 hashing

---

## 📦 Installation

### From PyPI

```bash
pip install vcs-core
```

### Local Installation

```bash
# Clone the repository
git clone https://github.com/ZEUS33776/vcs.git
cd vcs

# Install the package
pip install .
```

### Verify Installation

```bash
vcs --help
```

---

## 📖 Commands

### `vcs init`

Initialize a new VCS repository in the current directory.

```bash
vcs init
```

**How it works:**

- Creates a `.vcs/` directory with necessary subdirectories (`objects`, `commits`, etc.)
- Sets up essential files like `HEAD` and `index` to start tracking
- Establishes the foundation for version control in your project

### `vcs auth <username> <email>`

Set user credentials that will be stored in the config file.

```bash
vcs auth john_doe john@example.com
```

**How it works:**

- Stores the username and email in `.vcs/config` for subsequent operations
- Required for commit operations to identify the author

### `vcs add <file>`

Stage a file for the next commit.

```bash
vcs add filename.txt
```

**How it works:**

- Stages changes by hashing the file's contents into a blob object
- Updates the `index` to track the file and its hash (prepares for commit)
- Think of this as telling VCS: "I want this file to be part of the next commit"

### `vcs commit "<message>"`

Create a new commit with staged changes.

```bash
vcs commit "Initial commit"
```

**How it works:**

- Creates a new commit object with:
  - A tree object representing the snapshot of all files staged (from the index)
  - Metadata like the commit message, author, timestamp
- Stores the commit object compressed in `.vcs/objects`
- Updates `HEAD` to point to this new commit hash
- Saves the snapshot, so you can revert or checkout later

### `vcs log`

Display the commit history.

```bash
vcs log
```

**How it works:**

- Shows the history of commits starting from `HEAD`
- Displays chronological list with hash, author, timestamp, and message
- Useful to track changes over time and review commit messages

### `vcs show <commit_hash>`

Show detailed information about a specific commit.

```bash
vcs show a1b2c3d4
# or
vcs show HEAD
```

**How it works:**

- Retrieves the commit object from storage
- Displays commit metadata and associated file changes
- Helps you understand what changed in a specific commit

### `vcs checkout <commit_hash>`

Switch the working directory to a specific commit.

```bash
vcs checkout a1b2c3d4
```

**How it works:**

- Switches your working directory to reflect the snapshot of the specified commit
- Deletes files that don't exist in the commit and restores files from the commit tree
- Updates `HEAD` to point to the commit
- Allows you to view or work with your project at any point in history

---

## 💡 Usage Examples

### Basic Workflow

```bash
# Initialize repository
vcs init

# Set user credentials
vcs auth alice alice@example.com

# Create and add a file
echo "Hello World" > hello.txt
vcs add hello.txt

# Commit the changes
vcs commit "Add hello.txt"

# Make changes and commit again
echo "Updated content" >> hello.txt
vcs add hello.txt
vcs commit "Update hello.txt"

# View history
vcs log

# Check out previous version
vcs checkout <first_commit_hash>
```

### Working with Multiple Files

```bash
# Add multiple files
echo "File 1" > file1.txt
echo "File 2" > file2.txt
vcs add file1.txt
vcs add file2.txt
vcs commit "Add two files"

# Show latest commit details
vcs show HEAD
```

---

## 📁 Project Structure

```
project/
├── .vcs/                    # VCS repository data
│   ├── objects/             # Compressed blob and tree objects
│   ├── commits/             # Commit objects
│   ├── index                # Staging area
│   ├── HEAD                 # Current commit reference
│   └── config               # Authentication and settings
└── vcs/                     # Source code
    ├── __init__.py
    ├── main.py             # CLI entry point
    └── commands/           # Command implementations
        ├── init.py
        ├── auth.py
        ├── add.py
        ├── commit.py
        ├── log.py
        ├── show.py
        └── checkout.py
```

---

## 🔍 How It Works

### Object Storage

- **Blobs**: Store file contents, compressed with zlib
- **Trees**: Store directory structures and file metadata
- **Commits**: Store commit metadata and tree references

### Authentication

- Username and email stored in `.vcs/config`
- Required for commit operations
- Set once using `vcs auth <username> <email>`

### Data Flow

1. **Add**: File content → Blob object → Index entry
2. **Commit**: Index entries → Tree object → Commit object → Update HEAD
3. **Checkout**: Commit hash → Tree object → Restore files

### File Organization

```
.vcs/
├── objects/           # Content-addressable storage
├── commits/           # Commit metadata
├── index              # Staging area (JSON)
├── HEAD               # Current commit pointer
└── config             # User credentials
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings for functions
- Include error handling

---

## 📄 License

MIT License

---

**Author: Arjun Deshmukh**

Thank you for using VCS!
