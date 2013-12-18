import java.util.Arrays;

class Conway
{
    public static void main(String[] args)
    {
	Grid game1 = new Grid(17);
	game1.pulsarGrid();
	game1.playn(30, 0.3);
    }
}

class Grid
{
    int [][] state;
    int [][] neighbors;

    Grid(int length)
    {
	state = new int [length][length];
	neighbors = new int [length][length];
    }

    void playn(int n, double waitTime)
    //Plays n turns of the Game of Life
    //Waits waitTime seconds between turns
    {
	for (int i = 0; i <= n; i++)
	    {
		try{
		    System.out.println("Turn " + i);
		    printArrayBlocks(state);
		    play1();
		    Thread.sleep((int)(waitTime * 1000));
		}
		catch(InterruptedException ex){
		    Thread.currentThread().interrupt();
		}
	    }
    }

    void play1()
    //Plays 1 turn of the Game of Life
    {
	neighbors = livingNeighbors();

	for (int i = 0; i <state.length; i++)
	    for (int j = 0; j <state[i].length; j++){
		if (state[i][j] == 1)
		    if ((neighbors[i][j] < 2) || (neighbors[i][j] > 3))
			state[i][j] = 0;
		if ((state[i][j] == 0) && (neighbors[i][j] == 3))
		    state[i][j] = 1;
		}
    }

    void printArray(int [][]a)
    {
	for (int i = 0; i < a.length; i++){
	    for (int j = 0; j < a[i].length; j++)
		System.out.print(a[i][j] + " ");
	    System.out.println("");
	}
    }

    void printArrayBlocks(int [][]a)
    //Prints an array using special unicode blocks
    {
	StringBuffer s = new StringBuffer();
	for (int i = 0; i < a.length; i++){
	    for (int j = 0; j < a[i].length; j++){
		if(a[i][j] == 1){
		    s.append("\u25A0 ");
		    continue;
		}
		s.append("\u25A1 ");
	    }
	    s.append("\n");
	}
	System.out.println(s);
    }
    
    void setLiving(int i, int j)
    //sets state[i][j] to 1
    {
	state[i][j] = 1;
    }

    int[][] livingNeighbors()
    //Returns an array with the same dimensions as state.
    //The value in each cell represents the number of living neighbors
    //the corresponding cell in state has.
    {
	int[][] n = new int [state.length][state.length];

	for (int i = 0; i < state.length; i++)
	    for (int j = 0; j <state[i].length; j++){
		if (state[i][j] == 1){
		    if (i == 0 && j == 0){
			n[i][j+1] += 1;
			n[i+1][j+1] += 1;
			n[i+1][j] += 1;
			continue;
		    }
		    if (i == 0 && j == (state[i].length - 1)){
			n[i][j-1] += 1;
			n[i+1][j-1] += 1;
			n[i+1][j] += 1;
			continue;
		    }
		    if (i == (state.length - 1) && j == 0){
			n[i-1][j] += 1;
			n[i-1][j+1] += 1;
			n[i][j+1] += 1;
			continue;
		    }
		    if (i == (state.length - 1) && j == (state[i].length - 1)){
			n[i-1][j-1] += 1;
			n[i-1][j] += 1;
			n[i][j-1] += 1;
			continue;
		    }
		    if (i == 0){
			n[i][j-1] += 1;
			n[i][j+1] += 1;
			n[i+1][j-1] += 1;
			n[i+1][j] += 1;
			n[i+1][j+1] += 1;
			continue;
		    }		    
		    if (i == (state.length - 1)){
			n[i][j-1] += 1;
			n[i][j+1] += 1;
			n[i-1][j-1] += 1;
			n[i-1][j] += 1;
			n[i-1][j+1] += 1;
			continue;
		    }	
		    if (j == 0){
			n[i-1][j] += 1;
			n[i+1][j] += 1;
			n[i-1][j+1] += 1;
			n[i][j+1] += 1;
			n[i+1][j+1] += 1;
			continue;
		    }		    	    	
		    if (j == (state[i].length - 1)){
			n[i-1][j] += 1;
			n[i+1][j] += 1;
			n[i-1][j-1] += 1;
			n[i][j-1] += 1;
			n[i+1][j-1] += 1;
			continue;
		    }
		    	
		    n[i-1][j-1] += 1;
		    n[i-1][j] += 1;
		    n[i-1][j+1] += 1;
		    n[i][j-1] += 1;
		    n[i][j+1] += 1;
		    n[i+1][j-1] += 1;
		    n[i+1][j] += 1;
		    n[i+1][j+1] += 1;
		}
	    }
	return n;
    }

    void pulsarGrid()
    //Returns a cammon GoL oscillator: The Pulsar
    {
	//Quadrant 1
	setLiving(2,4);
	setLiving(2,5);
	setLiving(2,6);
	setLiving(7,4);
	setLiving(7,5);
	setLiving(7,6);

	setLiving(4,7);
	setLiving(5,7);
	setLiving(6,7);
	setLiving(4,2);
	setLiving(5,2);
	setLiving(6,2);

	//Quadrant 2
	setLiving(2,10);
	setLiving(2,11);
	setLiving(2,12);
	setLiving(7,10);
	setLiving(7,11);
	setLiving(7,12);

	setLiving(4,9);
	setLiving(5,9);
	setLiving(6,9);
	setLiving(4,14);
	setLiving(5,14);
	setLiving(6,14);

	//Quadrant 3
	setLiving(9,10);
	setLiving(9,11);
	setLiving(9,12);
	setLiving(14,10);
	setLiving(14,11);
	setLiving(14,12);

	setLiving(10,9);
	setLiving(11,9);
	setLiving(12,9);
	setLiving(10,14);
	setLiving(11,14);
	setLiving(12,14);

	//Quadrant 4
	setLiving(9,4);
	setLiving(9,5);
	setLiving(9,6);
	setLiving(14,4);
	setLiving(14,5);
	setLiving(14,6);

	setLiving(10,7);
	setLiving(11,7);
	setLiving(12,7);
	setLiving(10,2);
	setLiving(11,2);
	setLiving(12,2);	
    }
}