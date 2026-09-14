# 15. Tecnologie Streaming, Media e Broadcast

## Cos'è e perché conta

L'ingegneria del software applicata al mondo **Media, OTT (Over-The-Top), Broadcast e Video Streaming** (es. piattaforme stile Netflix, DAZN, Sky, Twitch o piattaforme di live shopping e media asset management) affronta sfide estreme di scalabilità, throughput di rete, latenza e caching. Uno sviluppatore backend Senior deve comprendere l'intera **Media Pipeline**: dall'ingestion del segnale video grezzo alla transcodifica, dal packaging adattivo (HLS/DASH) alla distribuzione geografica su CDN, fino alla gestione di DRM, metadati sincronizzati e inserimento pubblicitario.

---

## 1. La Media Pipeline End-to-End

```
                      END-TO-END VIDEO STREAMING PIPELINE
  ┌──────────────┐      RTMP / SRT      ┌─────────────────────────┐
  │ Camera / Live│ ───────────────────► │ Ingestion & Transcoding │
  │ Video Source │                      │ (FFmpeg / AWS Elemental)│
  └──────────────┘                      └────────────┬────────────┘
                                                     │ Multi-bitrate (fMP4)
                                                     ▼
  ┌──────────────┐     HLS / DASH       ┌─────────────────────────┐
  │ Video Player │ ◄─────────────────── │ Packaging & DRM Engine  │
  │ (Web/Mobile) │                      │ (Widevine / FairPlay)   │
  └──────┬───────┘                      └────────────┬────────────┘
         │                                           │ Segments (.m4s, .ts)
         └───────────────────┐                       ▼
                             │           ┌─────────────────────────┐
                             └─────────► │ CDN Edge Caching        │
                                         │ (CloudFront / Akamai)   │
                                         └─────────────────────────┘
```

### Le Fasi della Pipeline:
1. **Ingestion (Acquisizione)**: La sorgente video (es. regia broadcast o encoder live) invia il flusso grezzo via protocolli a bassa latenza (SRT, RTMP) verso i server di acquisizione.
2. **Transcoding & Encoding (Transcodifica)**: Il flusso sorgente ad altissimo bitrate viene decodificato e ricompresso in più risoluzioni e bitrate (*Rendition Ladder*: es. 1080p a 5 Mbps, 720p a 2.5 Mbps, 480p a 1 Mbps, 360p a 500 Kbps) utilizzando codec moderni.
3. **Packaging**: Il video transcodificato viene spezzettato in piccoli file temporali (*Chunks / Segments* di 2-6 secondi) e vengono generati i file indice (*Manifest*).
4. **DRM & Encryption (Protezione del Contenuto)**: Cifratura dei segmenti video con AES-128 e integrazione con server di licenze DRM.
5. **CDN Distribution**: I segmenti video e i manifest vengono memorizzati e distribuiti sui nodi Edge delle CDN mondiali.
6. **Playback & ABR**: Il player sul dispositivo client seleziona dinamicamente il bitrate ottimale in base alla banda disponibile (*Adaptive Bitrate Streaming*).

---

## 2. Codecs, Container e Formati

* **Codec Video**:
  * **H.264 / AVC**: Lo standard universale compatibile con il 99.9% dei dispositivi.
  * **H.265 / HEVC**: Efficienza di compressione doppia rispetto ad H.264 (fondamentale per flussi 4K/UHD e HDR).
  * **AV1 / VP9**: Codec open-source ad altissima efficienza (supportati da YouTube, Netflix, Chrome).
* **Codec Audio**: **AAC** (Advanced Audio Coding), **Opus** (bassa latenza), **Dolby Digital Plus (E-AC-3)** (audio surround multicanale).
* **Formati Container**:
  * **fMP4 (Fragmented MP4 / CMAF)**: Standard moderno universale; separa i video in un file di inizializzazione (`init.mp4`) e singoli frammenti temporali indipendenti (`.m4s`).
  * **MPEG-2 TS (`.ts`)**: Container legacy a pacchetti da 188 byte storicamente usato da HLS.

---

## 3. Protocolli di Streaming: HLS vs MPEG-DASH vs WebRTC

```
┌───────────────┬────────────────────────────┬─────────────────────────────┬───────────────────────────┐
│ Caratteristica│ HLS (HTTP Live Streaming)  │ MPEG-DASH                   │ WebRTC                    │
├───────────────┼────────────────────────────┼─────────────────────────────┼───────────────────────────┤
│ **Creatore**  │ Apple (Standard IETF)      │ Standard Internazionale ISO │ W3C / IETF                │
│ **Manifest**  │ `.m3u8` (Playlist M3U)     │ `.mpd` (XML Presentation)   │ Nessuno (Signaling SDP)   │
│ **Segmenti**  │ `.ts`, `.m4s` (fMP4/CMAF)  │ `.mp4`, `.m4s` (fMP4/CMAF)  │ Nessun segmento (RTP/SRTP)│
│ **Latenza**   │ 6 - 30 sec (Standard)      │ 6 - 30 sec (Standard)       │ **< 500 ms (Sub-second)** │
│               │ 2 - 4 sec (LL-HLS)         │ 2 - 4 sec (LL-DASH)         │                           │
│ **Trasporto** │ HTTP/1.1, HTTP/2, HTTP/3   │ HTTP/1.1, HTTP/2, HTTP/3    │ UDP (SRTP con ICE/STUN)   │
│ **Scalabilità**│ **Massima (Cache su CDN)** │ **Massima (Cache su CDN)**  │ Media (Richiede SFU/MCU)  │
│ **Uso Tipico**│ OTT, Live TV, Video On Dem.│ Smart TV, Android, Web OTT  │ Live Betting, Aste, Meet  │
└───────────────┴────────────────────────────┴─────────────────────────────┴───────────────────────────┘
```

---

### HLS nel Dettaglio: Master Playlist e Media Playlist

Un flusso HLS è strutturato con una **Master Playlist** che elenca tutte le varianti di qualità (risoluzioni e bitrate) e rimanda a singole **Media Playlist**:

#### 1. Master Playlist (`master.m3u8`):
```m3u
#EXTM3U
#EXT-X-VERSION:6
#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080,CODECS="avc1.64002a,mp4a.40.2"
1080p/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2500000,RESOLUTION=1280x720,CODECS="avc1.4d401f,mp4a.40.2"
720p/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360,CODECS="avc1.42e01e,mp4a.40.2"
360p/index.m3u8
```

#### 2. Media Playlist per 1080p (`1080p/index.m3u8`):
```m3u
#EXTM3U
#EXT-X-VERSION:6
#EXT-X-TARGETDURATION:4
#EXT-X-MEDIA-SEQUENCE:101

#EXTINF:4.000,
segment_101.m4s
#EXTINF:4.000,
segment_102.m4s
#EXTINF:4.000,
segment_103.m4s
```

---

### Adaptive Bitrate Streaming (ABR)

L'algoritmo ABR implementato nel player client monitora continuamente:
1. **Throughput di download stimato**: Tempo impiegato per scaricare l'ultimo segmento video.
2. **Buffer Occupancy (Livello di riempimento del buffer)**: Secondi di video già scaricati e pronti in RAM.
3. Se la banda cala o il buffer si svuota, il player passa senza interruzioni (*seamlessly*) alla playlist con bitrate inferiore; non appena la rete torna stabile, effettua un *upscale* alla qualità superiore.

---

### Low-Latency Streaming: LL-HLS & Chunked Transfer

Nel broadcast tradizionale via HTTP, la latenza tipica è di 15-30 secondi (il player attende di avere 3 segmenti da 6 secondi nel buffer).
* **LL-HLS (Low-Latency HLS)**:
  * Divide ogni segmento in micro-frammenti (**Partial Segments / Chunks** da 200-300 ms).
  * Il server invia i partial segment al client man mano che vengono codificati tramite **HTTP/2 Chunked Transfer Encoding**, abbattendo la latenza a **2-3 secondi** (pari o inferiore al broadcast televisivo satellitare).

---

## 4. Content Protection: DRM (Digital Rights Management)

Per impedire la pirateria e rispettare i contratti dei content provider (Hollywood studio, leghe sportive), i media OTT utilizzano standard di cifratura e DRM:

* **CMAF & Common Encryption (CENC - ISO/IEC 23001-7)**:
  * Il file video viene cifrato una sola volta con algoritmo AES-128 in modalità CTR o CBCS.
  * Il file cifrato può essere decifrato da diversi sistemi DRM compatibili:
    * **Google Widevine**: Utilizzato su Android, Chrome, Smart TV Android/Google.
    * **Apple FairPlay**: Utilizzato su iOS, iPadOS, macOS, Safari, Apple TV.
    * **Microsoft PlayReady**: Utilizzato su Windows, Edge, Xbox.

---

## 5. Inserimento Pubblicitario e Metadati Sincronizzati

* **SSAI (Server-Side Ad Insertion / Dynamic Ad Insertion - DAI)**:
  * Il backend cuce dinamicamente gli spot pubblicitari direttamente nel flusso video (manifest e segmenti) personalizzandoli per singolo utente.
  * **Vantaggi**: Impossibile da bloccare con gli *Ad-Blocker* tradizionali, transizione fluida senza lag nel player.
* **CSAI (Client-Side Ad Insertion)**:
  * Il player client interrompe il video e richiede lo spot a un server ad-server (es. via protocolli VAST/VMAP).
* **SCTE-35 & ID3 Metadata**:
  * Segnali digitali incorporati nel flusso broadcast per indicare con precisione al millisecondo l'inizio e la fine dei break pubblicitari (*Cue-In / Cue-Out*).

---

## 6. Domande tipiche a colloquio (e risposte da Senior)

- *D: Come funziona l'Adaptive Bitrate Streaming (ABR) e perché i segmenti video devono essere allineati temporalmente su tutte le qualità?*
  - **R**: In ABR il player client seleziona dinamicamente il bitrate più idoneo misurando la banda e la capienza del buffer. Affinché il cambio di qualità avvenga in modo trasparente e senza scatti (*seamless switching*), tutti i segmenti video di tutte le risoluzioni devono avere la **stessa durata temporale esatta** e iniziare con un **Keyframe (I-Frame / IDR frame)** allineato al millisecondo, consentendo al decoder di riprodurre il nuovo segmento senza dover ricalcolare i frame precedenti.

- *D: Qual è la differenza tra HLS/DASH e WebRTC, e quando sceglieresti WebRTC?*
  - **R**: HLS e DASH si basano su HTTP/TCP e architettura a segmenti: sfruttano le cache delle CDN standard permettendo di scalare a milioni di spettatori contemporanei con latenze tra 2 e 15 secondi. WebRTC si basa su UDP (SRTP) e streaming continuo senza segmentazione, offrendo latenza **sub-secondo (< 500 ms)**. Sceglierei WebRTC per applicazioni interattive real-time (aste live, scommesse in-play, videochiamate, cloud gaming), mentre per grandi eventi sportivi broadcast con milioni di utenti si preferisce LL-HLS/DASH per l'imbattibile scalabilità e costi delle CDN.

- *D: Come gestisci il caching a livello di CDN per i file manifest rispetto ai segmenti video?*
  - **R**: I **segmenti video** (`.m4s` o `.ts`) sono immutabili e vengono memorizzati in cache sulla CDN con un `Cache-Control: public, max-age=31536000` (1 anno) per massimizzare il cache-hit ratio. Al contrario, i **manifest di flussi live** (`.m3u8` o `.mpd`) cambiano continuamente perché vengono aggiunti nuovi segmenti ogni pochi secondi: su di essi si imposta una cache brevissima (`max-age=1` o `no-cache`), assicurando che i player ricevano sempre l'aggiornamento dell'ultimo segmento live disponibile.
