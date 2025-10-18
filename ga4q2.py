import tiktoken

def count_chat_tokens(messages, model="gpt-4o-mini"):
    """
    Counts tokens for a list of messages (chat format) as GPT-4o-Mini would see them.
    """
    encoding = tiktoken.encoding_for_model(model)
    tokens_per_message = 3  # GPT chat models add ~3 tokens per message
    tokens_per_name = 1     # add 1 token if 'name' field is used

    total_tokens = 0
    for msg in messages:
        total_tokens += tokens_per_message
        for key, value in msg.items():
            total_tokens += len(encoding.encode(value))
            if key == "name":
                total_tokens += tokens_per_name
    total_tokens += 3  # additional tokens for reply priming
    return total_tokens

# Your test message
messages = [
    {"role": "user", "content": "List only the valid English words from these: N7ltXYTlRG, StS4gr, yxwfpvn, 7pIY, UzX3C0h, tW, QId, SQ, hdHxeh, dVakTAcj, 2dh1P7LYq, B79WS6J, Bfn, elPwiYlL, raGk, mkMb5OsJIY, 1HzQLO, 1o, g, 07nNON, fMmF1CnP, Xvl, ERG3, T, NRtw, I, sPtSF7, wf427x4, Afndzq, cupYoP8mR1, yne9ZxE, HGzA, C8Hi, AtIN44, RBEAUyH, wl, 31eKtapFD, y, lGEM6xfS, a2, ga04jmA1di, zd, nu42q1SVnZ, nc, zEEYHf, vlKt, 3jig8r, ofH, IE, KAF0, ECENLBqP, TH, ADWl2VC, P, CNCNh7AXh, NWoKDxGL, caf, L, IJEul7cqa, yHN9ka, xA, 9kIXSGYD, xBQ, hwE33Z4by, yy4kKbSdO, KDMHBvy1t, Pce, NwZnuJ, ZO2i2D, hEVoule0w, uyk10WCc, N, 0h, pJ, Jyz0mRJHn, u, LFyRjgYsUO, SMowvI, tKnW0, Gd3h8j, zY5w1, tF, s, Q, 74LRRzI, VJP5, oDs, 9LKkb, iUN18sEO"}
]

total_tokens = count_chat_tokens(messages)
print("Exact input tokens:", total_tokens)