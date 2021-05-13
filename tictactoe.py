from PIL import Image
from decouple import config
import pyimgur


class TicTac:
    imgurid = config('IMGUR_ID')
    im = pyimgur.Imgur(imgurid)

    def __init__(self):
        self.playboard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.brd = Image.open("tictac/board2.png")

    # Return url to empty board
    def board(self):
        img = self.im.upload_image("tictac/board2.png", title="board")
        return img.link

    # Determine winner
    def checkwin(self, symbol, square):
        start = [0, 3, 6, 0, 1]
        increment = [1, 1, 1, 4, 2]
        vertical = [0, 3, 6]
        size = 3
        if symbol == '🇽':
            self.playboard[square-1] = 1
        elif symbol == '🇴':
            self.playboard[square-1] = -1
        # Check Horizontal and Both Diagonals
        for i in range(5):
            ans = 0
            for j in range(3):
                ind = (start[i]+j)*increment[i]
                ans += self.playboard[ind]
            if abs(ans) == size:
                return ans/size
        # Check Vertical
        for k in range(3):
            ans = 0
            for l in vertical:
                ind = l+k
                ans += self.playboard[ind]
            if abs(ans) == size:
                return ans/size
        for k in self.playboard:
            if k != 0:
                continue
            else:
                return 2
        return 0

    # Combine move image with current board state image and return url
    def move(self, symbol, square):
        if symbol == '🇽':
            symbol = 'x'
        elif symbol == '🇴':
            symbol = 'o'

        moveimg = Image.open(f"tictac/{symbol}{square}.png")
        self.brd.paste(moveimg, (0, 0), moveimg)
        self.brd.save('temp.png', format='PNG')
        moveimgur = self.im.upload_image("temp.png", title=f"{symbol}{square}move")
        return moveimgur.link
