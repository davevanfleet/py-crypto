def calc(ohlc_data):
    total_gains = 0
    total_losses = 0
    for i in range(1, 14):
        if float(ohlc_data[i][4]) > float(ohlc_data[i - 1][4]):
            total_gains += float(ohlc_data[i][4]) - float(ohlc_data[i - 1][4])
        else:
            total_losses += float(ohlc_data[i][4]) - float(ohlc_data[i - 1][4])
    average_gains = abs(total_gains / 14)
    average_losses = abs(total_losses / 14)
    for i in range(14, len(ohlc_data)):
        current_close = float(ohlc_data[i][4])
        previous_close = float(ohlc_data[i - 1][4])
        current_gain = max((current_close - previous_close), 0)
        current_loss = max(((current_close - previous_close) * -1), 0)
        average_gains = ((average_gains * 13) + current_gain) / 14
        average_losses = ((average_losses * 13) + current_loss) / 14
    
    return 100 - (100 / (1 + (average_gains / average_losses)))