# Custom Personality Creator

When the user picks "Custom" or says "create a personality," run this creator.

## Steps

1. **Ask for the concept.** Use AskUserQuestion or just ask:
   ```
   🎨 **Custom Personality Creator**

   Describe the voice you want. Can be:
   - A real person: "Gordon Ramsay" "Bob Ross" "David Attenborough"
   - A character type: "a disappointed TypeScript compiler" "your mom reading your code" "a medieval knight"
   - A vibe: "surfer bro" "corporate email" "dramatic movie trailer narrator"

   Who should roast your code?
   ```

2. **Generate the personality spec.** Based on their description, generate a personality definition following the same format as the built-in packs:
   - **Name and emoji** — pick an appropriate emoji
   - **Voice description** — 2-3 sentences defining the tone, vocabulary, and style
   - **Example roast lines** — write 3 sample roast lines in this voice so the user can preview
   - **What to avoid** — things that would break character

3. **Preview and confirm.** Show the user the personality spec with the 3 sample lines. Ask:
   ```
   Here's your custom personality:

   [emoji] **[name]**
   [voice description]

   Sample roast lines:
   - "[example 1]"
   - "[example 2]"
   - "[example 3]"

   Use this personality? (yes / tweak it / start over)
   ```

4. **Save if they want.** After confirming, offer to save:
   ```
   💾 Save this personality for future roasts?
   I'll write it to `.blunt-cake/custom-personalities/[name].md` so you can reuse it.
   ```
   If yes, save the personality spec as a markdown file. On future triggers, list saved custom personalities alongside the built-in packs.

5. **Proceed with the roast** using the custom personality, following the same rules as built-in packs — voice changes, substance doesn't.

## Loading Saved Custom Personalities

On skill trigger, check if `.blunt-cake/custom-personalities/` exists in the project root or home directory. If it does, list any saved personalities alongside the built-in packs in the picker:
```
🧑‍🍳 Chef (default) · 👵 Disappointed Grandma · ... · 🏴‍☠️ Pirate
🎨 Custom: 🤖 Disappointed TypeScript Compiler · 🎬 Movie Trailer Guy
```
