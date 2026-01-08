{
  "patcher": {
    "fileversion": 1,
    "appversion": {
      "major": 8,
      "minor": 6,
      "revision": 0,
      "architecture": "x64",
      "modernui": 1
    },
    "rect": [
      100.0,
      100.0,
      1100.0,
      750.0
    ],
    "bglocked": 0,
    "boxes": [
      {
        "box": {
          "id": "main_vocals_panel",
          "maxclass": "panel",
          "patching_rect": [
            15.0,
            15.0,
            340.0,
            170.0
          ],
          "bgcolor": [
            0.8,
            0.3,
            0.3,
            1.0
          ],
          "border": 1,
          "rounded": 10
        }
      },
      {
        "box": {
          "id": "backup_vocals_panel",
          "maxclass": "panel",
          "patching_rect": [
            15.0,
            195.0,
            340.0,
            170.0
          ],
          "bgcolor": [
            0.5,
            0.6,
            0.9,
            1.0
          ],
          "border": 1,
          "rounded": 10
        }
      },
      {
        "box": {
          "id": "instrumental_panel",
          "maxclass": "panel",
          "patching_rect": [
            15.0,
            375.0,
            340.0,
            170.0
          ],
          "bgcolor": [
            0.4,
            0.8,
            0.5,
            1.0
          ],
          "border": 1,
          "rounded": 10
        }
      },
      {
        "box": {
          "id": "main_vocals_label",
          "maxclass": "comment",
          "patching_rect": [
            25.0,
            25.0,
            150.0,
            20.0
          ],
          "text": "MAIN VOCALS",
          "fontsize": 12.0,
          "fontface": 1
        }
      },
      {
        "box": {
          "id": "main_vocals_vol_label",
          "maxclass": "comment",
          "patching_rect": [
            25.0,
            50.0,
            100.0,
            20.0
          ],
          "text": "Volume (dB)"
        }
      },
      {
        "box": {
          "id": "main_vocals_vol_num",
          "maxclass": "flonum",
          "patching_rect": [
            25.0,
            70.0,
            80.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "main_vocals_vol_pre",
          "maxclass": "newobj",
          "patching_rect": [
            115.0,
            70.0,
            220.0,
            22.0
          ],
          "text": "prepend main_vocals_volume_change"
        }
      },
      {
        "box": {
          "id": "main_vocals_filt_label",
          "maxclass": "comment",
          "patching_rect": [
            180.0,
            50.0,
            80.0,
            20.0
          ],
          "text": "Filter"
        }
      },
      {
        "box": {
          "id": "main_vocals_filt_num",
          "maxclass": "number",
          "patching_rect": [
            180.0,
            70.0,
            60.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "main_vocals_filt_pre",
          "maxclass": "newobj",
          "patching_rect": [
            250.0,
            70.0,
            130.0,
            22.0
          ],
          "text": "prepend filter_radius"
        }
      },
      {
        "box": {
          "id": "backup_vocals_label",
          "maxclass": "comment",
          "patching_rect": [
            25.0,
            205.0,
            150.0,
            20.0
          ],
          "text": "BACKUP VOCALS",
          "fontsize": 12.0,
          "fontface": 1
        }
      },
      {
        "box": {
          "id": "backup_vocals_vol_label",
          "maxclass": "comment",
          "patching_rect": [
            25.0,
            230.0,
            100.0,
            20.0
          ],
          "text": "Volume (dB)"
        }
      },
      {
        "box": {
          "id": "backup_vocals_vol_num",
          "maxclass": "flonum",
          "patching_rect": [
            25.0,
            250.0,
            80.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "backup_vocals_vol_pre",
          "maxclass": "newobj",
          "patching_rect": [
            115.0,
            250.0,
            230.0,
            22.0
          ],
          "text": "prepend backup_vocals_volume_change"
        }
      },
      {
        "box": {
          "id": "instrumental_label",
          "maxclass": "comment",
          "patching_rect": [
            25.0,
            385.0,
            150.0,
            20.0
          ],
          "text": "INSTRUMENTAL",
          "fontsize": 12.0,
          "fontface": 1
        }
      },
      {
        "box": {
          "id": "instrumental_vol_label",
          "maxclass": "comment",
          "patching_rect": [
            25.0,
            410.0,
            100.0,
            20.0
          ],
          "text": "Volume (dB)"
        }
      },
      {
        "box": {
          "id": "instrumental_vol_num",
          "maxclass": "flonum",
          "patching_rect": [
            25.0,
            430.0,
            80.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "instrumental_vol_pre",
          "maxclass": "newobj",
          "patching_rect": [
            115.0,
            430.0,
            220.0,
            22.0
          ],
          "text": "prepend instrumental_volume_change"
        }
      },
      {
        "box": {
          "id": "api_label",
          "maxclass": "comment",
          "text": "Replicate API Key",
          "patching_rect": [
            370.0,
            205.0,
            150.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "api",
          "maxclass": "textedit",
          "patching_rect": [
            370.0,
            225.0,
            300.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "api_pre",
          "maxclass": "newobj",
          "text": "prepend apikey",
          "patching_rect": [
            330.0,
            40.0,
            100.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "drop_label",
          "maxclass": "comment",
          "text": "Drop source WAV/MP3 here",
          "patching_rect": [
            370.0,
            425.0,
            200.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "drop",
          "maxclass": "dropfile",
          "patching_rect": [
            370.0,
            445.0,
            320.0,
            80.0
          ]
        }
      },
      {
        "box": {
          "id": "routepass",
          "maxclass": "newobj",
          "text": "route pass",
          "patching_rect": [
            330.0,
            120.0,
            70.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "defer",
          "maxclass": "newobj",
          "text": "deferlow",
          "patching_rect": [
            410.0,
            120.0,
            60.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "src_pre",
          "maxclass": "newobj",
          "text": "prepend source",
          "patching_rect": [
            480.0,
            120.0,
            100.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "model_label",
          "maxclass": "comment",
          "text": "Voice Model",
          "patching_rect": [
            370.0,
            150.0,
            180.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "model",
          "maxclass": "textedit",
          "patching_rect": [
            370.0,
            170.0,
            220.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "model_pre",
          "maxclass": "newobj",
          "text": "prepend rvc_model",
          "patching_rect": [
            230.0,
            200.0,
            120.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "url_label",
          "maxclass": "comment",
          "text": "custom_rvc_model_download_url (optional)",
          "patching_rect": [
            20.0,
            230.0,
            280.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "url",
          "maxclass": "textedit",
          "patching_rect": [
            20.0,
            250.0,
            330.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "url_pre",
          "maxclass": "newobj",
          "text": "prepend model_url",
          "patching_rect": [
            360.0,
            250.0,
            120.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "idx_label",
          "maxclass": "comment",
          "text": "Index Rate",
          "patching_rect": [
            370.0,
            315.0,
            150.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "idx_num",
          "maxclass": "flonum",
          "patching_rect": [
            370.0,
            335.0,
            80.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "idx_pre",
          "maxclass": "newobj",
          "text": "prepend index_rate",
          "patching_rect": [
            100.0,
            300.0,
            120.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "pitch_label",
          "maxclass": "comment",
          "text": "PITCH/OCTAVE (semitones)",
          "patching_rect": [
            370.0,
            75.0,
            200.0,
            22.0
          ],
          "fontsize": 12.0,
          "fontface": 1
        }
      },
      {
        "box": {
          "id": "pitch_num",
          "maxclass": "number",
          "patching_rect": [
            370.0,
            100.0,
            120.0,
            35.0
          ]
        }
      },
      {
        "box": {
          "id": "pitch_pre",
          "maxclass": "newobj",
          "text": "prepend pitch_change_all",
          "patching_rect": [
            320.0,
            300.0,
            160.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "btn",
          "maxclass": "textbutton",
          "text": "Process (per mode)",
          "patching_rect": [
            370.0,
            375.0,
            220.0,
            40.0
          ]
        }
      },
      {
        "box": {
          "id": "btn_msg",
          "maxclass": "message",
          "text": "process",
          "patching_rect": [
            180.0,
            340.0,
            60.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "node",
          "maxclass": "newobj",
          "text": "node.script @watch 0 rvc_unified.js",
          "patching_rect": [
            20.0,
            380.0,
            260.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "route",
          "maxclass": "newobj",
          "text": "route status progress done error",
          "patching_rect": [
            20.0,
            410.0,
            300.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "status",
          "maxclass": "message",
          "patching_rect": [
            20.0,
            620.0,
            700.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "prog",
          "maxclass": "slider",
          "patching_rect": [
            20.0,
            645.0,
            700.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "err",
          "maxclass": "message",
          "text": "(errors)",
          "patching_rect": [
            20.0,
            670.0,
            700.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "buf",
          "maxclass": "newobj",
          "text": "buffer~ resultbuf 44100 20000",
          "patching_rect": [
            500.0,
            380.0,
            220.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "wave",
          "maxclass": "waveform~",
          "patching_rect": [
            730.0,
            620.0,
            350.0,
            120.0
          ]
        }
      },
      {
        "box": {
          "id": "replace",
          "maxclass": "newobj",
          "text": "prepend replace",
          "patching_rect": [
            330.0,
            430.0,
            110.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "live_label",
          "maxclass": "comment",
          "text": "Auto-place into highlighted clip slot (Live)",
          "patching_rect": [
            500.0,
            540.0,
            320.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "liveobj",
          "maxclass": "newobj",
          "text": "live.object",
          "patching_rect": [
            500.0,
            600.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "livepath_msg",
          "maxclass": "message",
          "text": "path live_set view highlighted_clip_slot",
          "patching_rect": [
            500.0,
            570.0,
            280.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "drop_pre",
          "maxclass": "newobj",
          "text": "prepend call drop_sample",
          "patching_rect": [
            330.0,
            460.0,
            170.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "newtrack_label",
          "maxclass": "comment",
          "text": "Create new audio track + auto-target first empty slot",
          "patching_rect": [
            500.0,
            630.0,
            350.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "newtrack_btn",
          "maxclass": "textbutton",
          "text": "New Track Mode",
          "patching_rect": [
            500.0,
            650.0,
            120.0,
            24.0
          ]
        }
      },
      {
        "box": {
          "id": "newtrack_msg",
          "maxclass": "message",
          "text": "path live_set",
          "patching_rect": [
            500.0,
            680.0,
            120.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "liveobj_set",
          "maxclass": "newobj",
          "text": "live.object",
          "patching_rect": [
            630.0,
            680.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "call_create",
          "maxclass": "message",
          "text": "call create_audio_track",
          "patching_rect": [
            500.0,
            710.0,
            180.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "firstslot_path",
          "maxclass": "message",
          "text": "path live_set tracks 0 clip_slots 0",
          "patching_rect": [
            500.0,
            740.0,
            260.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "liveobj_slot",
          "maxclass": "newobj",
          "text": "live.object",
          "patching_rect": [
            770.0,
            740.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "drop_pre_slot",
          "maxclass": "newobj",
          "text": "prepend call drop_sample",
          "patching_rect": [
            330.0,
            490.0,
            170.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "lastpath_label",
          "maxclass": "comment",
          "text": "Last processed file path",
          "patching_rect": [
            500.0,
            530.0,
            200.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "lastpath",
          "maxclass": "message",
          "text": "(last path)",
          "patching_rect": [
            500.0,
            550.0,
            350.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "newtrack_label",
          "maxclass": "comment",
          "text": "Create NEW audio track and drop result into first slot",
          "patching_rect": [
            500.0,
            585.0,
            360.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "newtrack_btn",
          "maxclass": "textbutton",
          "text": "New track + drop result",
          "patching_rect": [
            500.0,
            605.0,
            190.0,
            24.0
          ]
        }
      },
      {
        "box": {
          "id": "tbb",
          "maxclass": "newobj",
          "text": "t b b b",
          "patching_rect": [
            700.0,
            605.0,
            70.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "live_set",
          "maxclass": "newobj",
          "text": "live.object",
          "patching_rect": [
            500.0,
            640.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "path_live_set",
          "maxclass": "message",
          "text": "path live_set",
          "patching_rect": [
            595.0,
            640.0,
            110.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "create_track",
          "maxclass": "message",
          "text": "call create_audio_track",
          "patching_rect": [
            500.0,
            670.0,
            170.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "get_tracks",
          "maxclass": "message",
          "text": "get count tracks",
          "patching_rect": [
            680.0,
            670.0,
            140.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "route_count",
          "maxclass": "newobj",
          "text": "route count",
          "patching_rect": [
            830.0,
            670.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "expr_lastidx",
          "maxclass": "newobj",
          "text": "expr $i1 - 1",
          "patching_rect": [
            930.0,
            670.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "sprintf_path",
          "maxclass": "newobj",
          "text": "sprintf path live_set tracks %ld clip_slots 0",
          "patching_rect": [
            1030.0,
            670.0,
            290.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "dropper",
          "maxclass": "newobj",
          "text": "live.object",
          "patching_rect": [
            1330.0,
            670.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "dropper_pre",
          "maxclass": "newobj",
          "text": "prepend call drop_sample",
          "patching_rect": [
            1190.0,
            700.0,
            170.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "t_bang_path",
          "maxclass": "newobj",
          "text": "t b",
          "patching_rect": [
            1030.0,
            700.0,
            40.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "mode_label",
          "maxclass": "comment",
          "text": "Destination Mode",
          "patching_rect": [
            20.0,
            530.0,
            150.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "mode_menu",
          "maxclass": "umenu",
          "items": [
            "Session clip (highlighted)",
            "Arrangement (at playhead)"
          ],
          "patching_rect": [
            20.0,
            550.0,
            230.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "mode_route",
          "maxclass": "newobj",
          "text": "sel 0 1",
          "patching_rect": [
            260.0,
            550.0,
            60.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "arr_label",
          "maxclass": "comment",
          "text": "Arrangement insertion controls",
          "patching_rect": [
            20.0,
            580.0,
            250.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "arr_live",
          "maxclass": "newobj",
          "text": "live.object",
          "patching_rect": [
            20.0,
            640.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "arr_path",
          "maxclass": "message",
          "text": "path live_set",
          "patching_rect": [
            115.0,
            640.0,
            110.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "arr_get_time",
          "maxclass": "message",
          "text": "get current_song_time",
          "patching_rect": [
            20.0,
            670.0,
            160.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "arr_route_time",
          "maxclass": "newobj",
          "text": "route current_song_time",
          "patching_rect": [
            190.0,
            670.0,
            170.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "arr_sprintf",
          "maxclass": "newobj",
          "text": "sprintf call insert_audio_file %s %f",
          "patching_rect": [
            370.0,
            670.0,
            260.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "arr_insert_btn",
          "maxclass": "textbutton",
          "text": "Insert at playhead",
          "patching_rect": [
            20.0,
            610.0,
            150.0,
            24.0
          ]
        }
      },
      {
        "box": {
          "id": "done_gate",
          "maxclass": "newobj",
          "text": "gate 2",
          "patching_rect": [
            330.0,
            520.0,
            60.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "mode_plus1",
          "maxclass": "newobj",
          "text": "+ 1",
          "patching_rect": [
            330.0,
            550.0,
            40.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "t_i",
          "maxclass": "newobj",
          "text": "t i",
          "patching_rect": [
            380.0,
            550.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "arr_trigger",
          "maxclass": "newobj",
          "text": "t b b b",
          "patching_rect": [
            430.0,
            520.0,
            70.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "outfmt_label",
          "maxclass": "comment",
          "text": "output_format",
          "patching_rect": [
            650.0,
            315.0,
            120.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "outfmt",
          "maxclass": "umenu",
          "items": [
            "wav",
            "mp3"
          ],
          "patching_rect": [
            650.0,
            335.0,
            100.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "outfmt_pre",
          "maxclass": "newobj",
          "text": "prepend output_format",
          "patching_rect": [
            130.0,
            350.0,
            150.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "pdalgo_label",
          "maxclass": "comment",
          "text": "Pitch Algorithm",
          "patching_rect": [
            460.0,
            315.0,
            180.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "pdalgo",
          "maxclass": "umenu",
          "items": [
            "rmvpe",
            "mangio-crepe"
          ],
          "patching_rect": [
            460.0,
            335.0,
            150.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "pdalgo_pre",
          "maxclass": "newobj",
          "text": "prepend pitch_detection_algorithm",
          "patching_rect": [
            180.0,
            400.0,
            220.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "protect_label",
          "maxclass": "comment",
          "text": "Protect",
          "patching_rect": [
            180.0,
            290.0,
            100.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "protect_num",
          "maxclass": "flonum",
          "patching_rect": [
            180.0,
            310.0,
            80.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "protect_pre",
          "maxclass": "newobj",
          "text": "prepend protect",
          "patching_rect": [
            100.0,
            450.0,
            120.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "rms_label",
          "maxclass": "comment",
          "text": "RMS Mix",
          "patching_rect": [
            25.0,
            290.0,
            100.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "rms_num",
          "maxclass": "flonum",
          "patching_rect": [
            25.0,
            310.0,
            80.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "rms_pre",
          "maxclass": "newobj",
          "text": "prepend rms_mix_rate",
          "patching_rect": [
            320.0,
            450.0,
            150.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "filt_label",
          "maxclass": "comment",
          "text": "Filter",
          "patching_rect": [
            180.0,
            110.0,
            100.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "filt_num",
          "maxclass": "number",
          "patching_rect": [
            180.0,
            130.0,
            60.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "filt_pre",
          "maxclass": "newobj",
          "text": "prepend filter_radius",
          "patching_rect": [
            320.0,
            350.0,
            150.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "takes_label",
          "maxclass": "comment",
          "text": "Takes history",
          "patching_rect": [
            500.0,
            730.0,
            140.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "takes",
          "maxclass": "umenu",
          "patching_rect": [
            500.0,
            750.0,
            420.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "takes_append",
          "maxclass": "newobj",
          "text": "prepend append",
          "patching_rect": [
            500.0,
            780.0,
            130.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "takes_out",
          "maxclass": "message",
          "text": "(selected take path)",
          "patching_rect": [
            640.0,
            780.0,
            250.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "takes_drop_pre",
          "maxclass": "newobj",
          "text": "prepend call drop_sample",
          "patching_rect": [
            900.0,
            780.0,
            170.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "takes_dropper",
          "maxclass": "newobj",
          "text": "live.object",
          "patching_rect": [
            1080.0,
            780.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "takes_path_msg",
          "maxclass": "message",
          "text": "path live_set view highlighted_clip_slot",
          "patching_rect": [
            1080.0,
            750.0,
            280.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "name_label",
          "maxclass": "comment",
          "text": "Take name",
          "patching_rect": [
            500.0,
            810.0,
            120.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "take_name",
          "maxclass": "textedit",
          "patching_rect": [
            500.0,
            830.0,
            220.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "color_label",
          "maxclass": "comment",
          "text": "Color index (0-69)",
          "patching_rect": [
            730.0,
            810.0,
            150.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "color_num",
          "maxclass": "number",
          "patching_rect": [
            730.0,
            830.0,
            70.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "clip_get_msg",
          "maxclass": "message",
          "text": "get clip",
          "patching_rect": [
            1170.0,
            700.0,
            80.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "clip_route",
          "maxclass": "newobj",
          "text": "route clip",
          "patching_rect": [
            1260.0,
            700.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "clip_id_route",
          "maxclass": "newobj",
          "text": "route id",
          "patching_rect": [
            1360.0,
            700.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "clip_obj",
          "maxclass": "newobj",
          "text": "live.object",
          "patching_rect": [
            1460.0,
            700.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "set_name",
          "maxclass": "newobj",
          "text": "prepend set name",
          "patching_rect": [
            930.0,
            830.0,
            140.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "set_color",
          "maxclass": "newobj",
          "text": "prepend set color",
          "patching_rect": [
            1080.0,
            830.0,
            140.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "apply_btn",
          "maxclass": "textbutton",
          "text": "Apply name & color to current slot clip",
          "patching_rect": [
            930.0,
            860.0,
            300.0,
            24.0
          ]
        }
      },
      {
        "box": {
          "id": "selclip_label",
          "maxclass": "comment",
          "text": "Arrangement: apply to selected (detail) clip",
          "patching_rect": [
            500.0,
            860.0,
            300.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "selclip_obj",
          "maxclass": "newobj",
          "text": "live.object",
          "patching_rect": [
            500.0,
            900.0,
            90.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "selclip_path",
          "maxclass": "message",
          "text": "path live_set view detail_clip",
          "patching_rect": [
            595.0,
            900.0,
            220.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "pitch_knob",
          "maxclass": "live.dial",
          "patching_rect": [
            260.0,
            336.0,
            80.0,
            80.0
          ],
          "floatoutput": 1,
          "parameter_enable": 1,
          "saved_attribute_attributes": {
            "parameter_longname": "Pitch Shift (semitones)",
            "parameter_shortname": "Pitch (st)",
            "parameter_mmin": -12.0,
            "parameter_mmax": 12.0,
            "parameter_initial": 0.0,
            "parameter_unitstyle": 0
          }
        }
      },
      {
        "box": {
          "id": "pitch_knob_label",
          "maxclass": "comment",
          "text": "Pitch Shift (semitones)",
          "patching_rect": [
            250.0,
            420.0,
            160.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "backend_label",
          "maxclass": "comment",
          "text": "Backend",
          "patching_rect": [
            370.0,
            15.0,
            120.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "backend_menu",
          "maxclass": "umenu",
          "items": [
            "Replicate",
            "Local"
          ],
          "patching_rect": [
            370.0,
            35.0,
            140.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "backend_pre",
          "maxclass": "newobj",
          "text": "prepend backend",
          "patching_rect": [
            150.0,
            15.0,
            120.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "server_label",
          "maxclass": "comment",
          "text": "Local server URL (http://host:8000)",
          "patching_rect": [
            370.0,
            260.0,
            240.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "server_text",
          "maxclass": "textedit",
          "patching_rect": [
            370.0,
            280.0,
            300.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "server_pre",
          "maxclass": "newobj",
          "text": "prepend server",
          "patching_rect": [
            290.0,
            65.0,
            120.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "stability_label",
          "maxclass": "comment",
          "text": "Stable Server",
          "patching_rect": [
            700.0,
            240.0,
            180.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "stability_url",
          "maxclass": "textedit",
          "patching_rect": [
            700.0,
            260.0,
            180.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "stability_pre",
          "maxclass": "newobj",
          "text": "prepend stability_server",
          "patching_rect": [
            290.0,
            160.0,
            170.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "stable_prompt_label",
          "maxclass": "comment",
          "text": "Stable prompt (optional for Stable Audio)",
          "patching_rect": [
            370.0,
            535.0,
            250.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "stable_prompt",
          "maxclass": "textedit",
          "patching_rect": [
            370.0,
            555.0,
            330.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "stable_prompt_pre",
          "maxclass": "newobj",
          "text": "prepend stable_prompt",
          "patching_rect": [
            360.0,
            300.0,
            160.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "process_mode_label",
          "maxclass": "comment",
          "text": "Processing Mode (Voice/RVC, UVR, Stable Audio)",
          "patching_rect": [
            520.0,
            15.0,
            250.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "process_mode_menu",
          "maxclass": "umenu",
          "items": [
            "Voice (RVC)",
            "UVR (all stems)",
            "Stable Audio"
          ],
          "patching_rect": [
            520.0,
            35.0,
            160.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "process_mode_pre",
          "maxclass": "newobj",
          "text": "prepend mode",
          "patching_rect": [
            510.0,
            15.0,
            120.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "uvr_model_label",
          "maxclass": "comment",
          "text": "UVR model (Demucs name)",
          "patching_rect": [
            700.0,
            75.0,
            180.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "uvr_model",
          "maxclass": "textedit",
          "patching_rect": [
            700.0,
            95.0,
            180.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "uvr_model_pre",
          "maxclass": "newobj",
          "text": "prepend uvr_model",
          "patching_rect": [
            550.0,
            65.0,
            130.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "uvr_shifts_label",
          "maxclass": "comment",
          "text": "UVR Shifts",
          "patching_rect": [
            700.0,
            130.0,
            180.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "uvr_shifts_num",
          "maxclass": "number",
          "patching_rect": [
            700.0,
            150.0,
            70.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "uvr_shifts_pre",
          "maxclass": "newobj",
          "text": "prepend uvr_shifts",
          "patching_rect": [
            440.0,
            115.0,
            140.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "uvr_segment_label",
          "maxclass": "comment",
          "text": "UVR Segment",
          "patching_rect": [
            700.0,
            185.0,
            180.0,
            20.0
          ]
        }
      },
      {
        "box": {
          "id": "uvr_segment_num",
          "maxclass": "flonum",
          "patching_rect": [
            700.0,
            205.0,
            70.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "uvr_segment_pre",
          "maxclass": "newobj",
          "text": "prepend uvr_segment",
          "patching_rect": [
            440.0,
            165.0,
            150.0,
            22.0
          ]
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "source": [
            "api",
            0
          ],
          "destination": [
            "api_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "api_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "drop",
            0
          ],
          "destination": [
            "routepass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "routepass",
            0
          ],
          "destination": [
            "defer",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "src_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "src_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "model",
            0
          ],
          "destination": [
            "model_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "model_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "url",
            0
          ],
          "destination": [
            "url_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "url_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "idx_num",
            0
          ],
          "destination": [
            "idx_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "idx_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "pitch_num",
            0
          ],
          "destination": [
            "pitch_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "pitch_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "btn",
            0
          ],
          "destination": [
            "btn_msg",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "btn_msg",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "node",
            0
          ],
          "destination": [
            "route",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "route",
            0
          ],
          "destination": [
            "status",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "route",
            1
          ],
          "destination": [
            "prog",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "route",
            2
          ],
          "destination": [
            "replace",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "route",
            3
          ],
          "destination": [
            "err",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "replace",
            0
          ],
          "destination": [
            "buf",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "buf",
            0
          ],
          "destination": [
            "wave",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "livepath_msg",
            0
          ],
          "destination": [
            "liveobj",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "route",
            2
          ],
          "destination": [
            "drop_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "drop_pre",
            0
          ],
          "destination": [
            "liveobj",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "newtrack_btn",
            0
          ],
          "destination": [
            "newtrack_msg",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "newtrack_msg",
            0
          ],
          "destination": [
            "liveobj_set",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "newtrack_btn",
            0
          ],
          "destination": [
            "call_create",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "call_create",
            0
          ],
          "destination": [
            "liveobj_set",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "firstslot_path",
            0
          ],
          "destination": [
            "liveobj_slot",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "route",
            2
          ],
          "destination": [
            "drop_pre_slot",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "drop_pre_slot",
            0
          ],
          "destination": [
            "liveobj_slot",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "route",
            2
          ],
          "destination": [
            "lastpath",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "newtrack_btn",
            0
          ],
          "destination": [
            "tbb",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tbb",
            0
          ],
          "destination": [
            "path_live_set",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tbb",
            1
          ],
          "destination": [
            "create_track",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tbb",
            2
          ],
          "destination": [
            "get_tracks",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "path_live_set",
            0
          ],
          "destination": [
            "live_set",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "create_track",
            0
          ],
          "destination": [
            "live_set",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "get_tracks",
            0
          ],
          "destination": [
            "live_set",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "live_set",
            0
          ],
          "destination": [
            "route_count",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "route_count",
            0
          ],
          "destination": [
            "expr_lastidx",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "expr_lastidx",
            0
          ],
          "destination": [
            "sprintf_path",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "sprintf_path",
            0
          ],
          "destination": [
            "dropper",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "sprintf_path",
            0
          ],
          "destination": [
            "t_bang_path",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "t_bang_path",
            0
          ],
          "destination": [
            "lastpath",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lastpath",
            0
          ],
          "destination": [
            "dropper_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "dropper_pre",
            0
          ],
          "destination": [
            "dropper",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "mode_menu",
            0
          ],
          "destination": [
            "mode_route",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "arr_insert_btn",
            0
          ],
          "destination": [
            "arr_path",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "arr_path",
            0
          ],
          "destination": [
            "arr_live",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "arr_insert_btn",
            0
          ],
          "destination": [
            "arr_get_time",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "arr_get_time",
            0
          ],
          "destination": [
            "arr_live",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "arr_live",
            0
          ],
          "destination": [
            "arr_route_time",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lastpath",
            0
          ],
          "destination": [
            "arr_sprintf",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "arr_route_time",
            0
          ],
          "destination": [
            "arr_sprintf",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "arr_sprintf",
            0
          ],
          "destination": [
            "arr_live",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "mode_route",
            0
          ],
          "destination": [
            "mode_plus1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "mode_menu",
            1
          ],
          "destination": [
            "mode_plus1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "mode_plus1",
            0
          ],
          "destination": [
            "t_i",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "t_i",
            0
          ],
          "destination": [
            "done_gate",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "route",
            2
          ],
          "destination": [
            "done_gate",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "done_gate",
            1
          ],
          "destination": [
            "arr_trigger",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "arr_trigger",
            0
          ],
          "destination": [
            "lastpath",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "arr_trigger",
            1
          ],
          "destination": [
            "arr_path",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "arr_trigger",
            2
          ],
          "destination": [
            "arr_get_time",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "outfmt",
            0
          ],
          "destination": [
            "outfmt_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "outfmt_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "pdalgo",
            0
          ],
          "destination": [
            "pdalgo_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "pdalgo_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "protect_num",
            0
          ],
          "destination": [
            "protect_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "protect_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "rms_num",
            0
          ],
          "destination": [
            "rms_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "rms_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "filt_num",
            0
          ],
          "destination": [
            "filt_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "filt_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "route",
            2
          ],
          "destination": [
            "takes_append",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "takes_append",
            0
          ],
          "destination": [
            "takes",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "takes",
            0
          ],
          "destination": [
            "takes_out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "takes_path_msg",
            0
          ],
          "destination": [
            "takes_dropper",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "takes_out",
            0
          ],
          "destination": [
            "takes_drop_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "takes_drop_pre",
            0
          ],
          "destination": [
            "takes_dropper",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "apply_btn",
            0
          ],
          "destination": [
            "takes_path_msg",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "apply_btn",
            0
          ],
          "destination": [
            "clip_get_msg",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "clip_get_msg",
            0
          ],
          "destination": [
            "takes_dropper",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "takes_dropper",
            0
          ],
          "destination": [
            "clip_route",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "clip_route",
            0
          ],
          "destination": [
            "clip_id_route",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "clip_id_route",
            0
          ],
          "destination": [
            "clip_obj",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "take_name",
            0
          ],
          "destination": [
            "set_name",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set_name",
            0
          ],
          "destination": [
            "clip_obj",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "color_num",
            0
          ],
          "destination": [
            "set_color",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set_color",
            0
          ],
          "destination": [
            "clip_obj",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "selclip_path",
            0
          ],
          "destination": [
            "selclip_obj",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "take_name",
            0
          ],
          "destination": [
            "set_name",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set_name",
            0
          ],
          "destination": [
            "selclip_obj",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "color_num",
            0
          ],
          "destination": [
            "set_color",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set_color",
            0
          ],
          "destination": [
            "selclip_obj",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "pitch_knob",
            0
          ],
          "destination": [
            "pitch_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "backend_menu",
            0
          ],
          "destination": [
            "backend_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "backend_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "server_text",
            0
          ],
          "destination": [
            "server_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "server_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "stability_url",
            0
          ],
          "destination": [
            "stability_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "stability_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "stable_prompt",
            0
          ],
          "destination": [
            "stable_prompt_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "stable_prompt_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "process_mode_menu",
            0
          ],
          "destination": [
            "process_mode_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "process_mode_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "uvr_model",
            0
          ],
          "destination": [
            "uvr_model_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "uvr_model_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "uvr_shifts_num",
            0
          ],
          "destination": [
            "uvr_shifts_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "uvr_shifts_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "uvr_segment_num",
            0
          ],
          "destination": [
            "uvr_segment_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "uvr_segment_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "main_vocals_vol_num",
            0
          ],
          "destination": [
            "main_vocals_vol_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "main_vocals_vol_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "main_vocals_filt_num",
            0
          ],
          "destination": [
            "main_vocals_filt_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "main_vocals_filt_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "backup_vocals_vol_num",
            0
          ],
          "destination": [
            "backup_vocals_vol_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "backup_vocals_vol_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "instrumental_vol_num",
            0
          ],
          "destination": [
            "instrumental_vol_pre",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "instrumental_vol_pre",
            0
          ],
          "destination": [
            "node",
            0
          ]
        }
      }
    ]
  }
}