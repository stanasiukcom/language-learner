# Configuration Directory

## ⚠️ IMPORTANT: Privacy & Security

**DO NOT commit personal configuration files to git!**

This directory contains:
- `config.example.yaml` - Template (safe to commit)
- `config.yaml` - Your personal config (gitignored)
- Any `*.yaml` files - User configs (gitignored except example)

---

## 🔒 Security Best Practices

1. **Never share your personal config files** - they may contain:
   - Google Drive file IDs (private links)
   - YouTube video IDs (potentially private)
   - Personal course information
   - File paths and names

2. **Use the example template:**
   ```bash
   cp config.example.yaml config.yaml
   # Edit config.yaml with your details
   ```

3. **Check before committing:**
   ```bash
   git status  # Verify no personal configs are staged
   ```

4. **All user configs are gitignored by default:**
   - `config/*.yaml` (except `config.example.yaml`)
   - `config/*_maciek.yaml`
   - `config/*_personal.yaml`
   - `config/*_private.yaml`

---

## 📝 Creating Your Config

```bash
# Copy the template
cp config.example.yaml config.yaml

# Or create a personal named config
cp config.example.yaml config/my_course.yaml

# Edit with your details
nano config.yaml
```

---

## ✅ Safe to Share

If you want to share a configuration example:
1. Remove all real file IDs
2. Replace with placeholders like `"YOUR_FILE_ID_HERE"`
3. Remove personal information (names, paths, etc.)
4. Save as a new example file in `examples/` directory

---

**Remember: Once data is pushed to GitHub, it's difficult to completely remove. Always verify before pushing!**
