# Spotify-YouTube Playlist Migrator 🎵

A Python package to easily migrate playlists between Spotify and YouTube Music with simple login.

---

## Features ✨

- **Easy Authentication** - Simply login with your Spotify and YouTube Music accounts
- Migrate Spotify playlists to YouTube Music
- Migrate YouTube Music playlists to Spotify
- Migrate Spotify Liked Songs to YouTube Music
- Detailed logging and migration statistics

---

## Installation 🛠️

1. Install the package via pip:
   ```bash
   pip install spotify-youtube-migrator
   ```

2. Ready to use! No separate API keys or credentials required.

---

## Usage 🚀

### Migrate Spotify Playlist to YouTube Music

```bash
migrate-playlist migrate --source spotify --destination youtube --playlist <playlist_url> --name "My Playlist"
```

### Migrate Spotify Liked Songs to YouTube Music

```bash
migrate-playlist migrate --source spotify --destination youtube --playlist liked_songs --name "My Liked Songs"
```

### Migrate YouTube Music Playlist to Spotify

```bash
migrate-playlist migrate --source youtube --destination spotify --playlist <playlist_url> --name "My Playlist"
```

### Check Authentication Status

```bash
migrate-playlist auth status
```

### Clear Authentication Data

```bash
migrate-playlist auth clear
```

### View Migration Statistics

Add the `--stats` flag to see details about the migration:

```bash
migrate-playlist migrate --source spotify --destination youtube --playlist <playlist_url> --stats
```

---

## Authentication Flow 🔐

The first time you run a migration command:

1. A browser window will open for you to log in to Spotify
2. After Spotify authentication, you'll be guided through YouTube Music authentication
3. Your authentication is securely stored for future use

---

## Commands 📜

| Command | Description |
|---------|-------------|
| `migrate --source <source>` | Migrate playlists between platforms |
| `--destination <destination>` | Specify the destination platform |
| `--playlist <url_or_liked_songs>` | Provide the playlist URL or use `liked_songs` for Spotify Liked Songs |
| `--name <playlist_name>` | Specify a custom name for the new playlist |
| `--log` | Enable detailed logging |
| `--stats` | Display migration statistics |
| `auth status` | Check authentication status for both services |
| `auth clear` | Clear saved authentication tokens |

---

## Contributing 🤝

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

---

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support 💬

If you encounter any issues or have questions, please open an issue on [GitHub](https://github.com/manojk0303/spotify-youtube-migrator/issues).