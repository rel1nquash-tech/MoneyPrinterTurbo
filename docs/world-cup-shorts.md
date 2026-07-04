# World Cup Shorts

The `worldcup_shorts` preset creates English, faceless, portrait shorts. It targets 30-50 seconds, enables subtitles, matches stock clips in script order, and supplies copyright-conscious B-roll search terms when no terms are entered.

## WebUI Workflow

1. Start MoneyPrinterTurbo and select **World Cup Shorts** under **Content Preset**.
2. Enter a subject that uses verified, non-live facts.
3. Paste an English narration into **Video Script**. About 75-110 spoken words is a useful starting range; actual duration depends on the selected voice and speed.
4. Keep the supplied generic stock terms, or replace them with your own generic English stock descriptions.
5. Select Pexels or Pixabay, choose an English TTS voice, and click **Generate Video**.

Pasting a script bypasses LLM script generation. The preset also supplies stock search terms, so this workflow does not need an OpenAI or other LLM API key. The optional **Generate Video Script and Keywords** button does use the configured LLM.

## Stock Provider Requirements

Online B-roll requires at least one provider key:

- Add a Pexels key to `pexels_api_keys` in the ignored local `config.toml`, or enter it in WebUI API key management.
- Add a Pixabay key to `pixabay_api_keys` in the ignored local `config.toml`, or enter it in WebUI API key management.
- Never put provider keys in source files, sample data, commits, or documentation.

The preset limits WebUI online sources to Pexels and Pixabay. A provider key is still required even when no LLM key is configured.

## TTS And Subtitles

The video pipeline needs narration audio. The default **Azure TTS V1** option is Edge TTS: it needs internet access but no API key. Paid or self-hosted TTS choices require their own configuration. Select an English voice and confirm it works with **Test Voice** before rendering.

Subtitles are enabled by the preset. With `subtitle_provider = "edge"`, Edge TTS timing is used. Whisper is optional and may download a local model.

## Copyright Safety

- Use generic stock scenes such as stadium exteriors, empty pitches, football training, supporters, flags, city views, boots, balls, and lights.
- Do not use broadcast recordings, official match footage, highlight reels, replay clips, or downloaded social-media edits.
- Avoid team crests, broadcast graphics, sponsor marks, and identifiable match close-ups unless you have permission.
- Review every downloaded asset and its provider license before publishing. Search terms reduce risk but do not replace a rights check.
- Verify historical facts from reliable sources. Do not present placeholders or unconfirmed current results as facts.

Topic scaffolds are available in `resource/worldcup/sample_topics.json`. Replace every bracketed placeholder with verified information before generating a script.

## First Test Video

1. Put one Pexels or Pixabay key in local `config.toml` or WebUI API key management.
2. Start the WebUI and select **World Cup Shorts**.
3. Use the subject `Why World Cup underdog stories stay memorable`.
4. Paste this manual script:

   > World Cup underdog stories endure because every match begins with possibility. A less-fancied team can stay compact, trust its preparation, and turn one brave moment into lasting history. The tension is not only about a score. It is about supporters realizing that reputation does not decide everything. When discipline, belief, and timing come together, the tournament gains a story people retell for years. That is why an unexpected run can become bigger than a single result.

5. Keep the default safe terms, select an English Edge TTS voice, and generate one video.
6. Confirm the result is portrait, roughly 30-50 seconds, readable with subtitles, and contains only acceptable stock footage before publishing.

The equivalent CLI flow is:

```powershell
python cli.py --video-subject "Why World Cup underdog stories stay memorable" --content-preset worldcup_shorts --video-script "Paste the manual English script here" --video-source pexels --voice-name "en-US-JennyNeural-Female"
```

The command prints the task ID and generated paths under `result.videos` when rendering succeeds.
